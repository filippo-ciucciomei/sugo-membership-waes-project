document.addEventListener("DOMContentLoaded", async function () {

    const gpxScript = document.getElementById("gpx-url");
    if (!gpxScript) return;

    const gpxUrl = JSON.parse(gpxScript.textContent);

    const map = L.map("ride-map");

    const startIcon = new L.Icon({
        iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    const finishIcon = new L.Icon({
        iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
        shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        maxZoom: 18,
        attribution: "&copy; OpenStreetMap contributors"
    }).addTo(map);

    function haversineDistance(lat1, lon1, lat2, lon2) {
        const R = 6371;
        const toRad = deg => deg * Math.PI / 180;

        const dLat = toRad(lat2 - lat1);
        const dLon = toRad(lon2 - lon1);

        const a =
            Math.sin(dLat / 2) * Math.sin(dLat / 2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon / 2) * Math.sin(dLon / 2);

        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
        return R * c;
    }

    try {

        const response = await fetch(gpxUrl);
        const gpxText = await response.text();

        const parser = new DOMParser();
        const xml = parser.parseFromString(gpxText, "application/xml");

        const trackPoints = xml.getElementsByTagName("trkpt");

        const latlngs = [];
        const distances = [];
        const elevations = [];

        let totalDistance = 0;
        let previousLat = null;
        let previousLon = null;
        let totalElevationGain = 0;
        let previousElevation = null;

        for (let i = 0; i < trackPoints.length; i++) {

            const point = trackPoints[i];
            const lat = parseFloat(point.getAttribute("lat"));
            const lon = parseFloat(point.getAttribute("lon"));

            const eleTag = point.getElementsByTagName("ele")[0];
            const ele = eleTag ? parseFloat(eleTag.textContent) : null;

            if (ele !== null && previousElevation !== null && ele > previousElevation) {
                totalElevationGain += (ele - previousElevation);
            }

            latlngs.push([lat, lon]);

            if (previousLat !== null && previousLon !== null) {
                totalDistance += haversineDistance(previousLat, previousLon, lat, lon);
            }

            distances.push(totalDistance.toFixed(2));
            elevations.push(ele);

            previousLat = lat;
            previousLon = lon;
            previousElevation = ele;
        }

        if (latlngs.length > 0) {

            document.getElementById("ride-distance").textContent = totalDistance.toFixed(1);
            document.getElementById("ride-elevation").textContent = Math.round(totalElevationGain);

            const polyline = L.polyline(latlngs, {
                color: "#e63946",
                weight: 5,
                opacity: 0.8
            }).addTo(map);
            map.fitBounds(polyline.getBounds());

            const startPoint = latlngs[0];
            const endPoint = latlngs[latlngs.length - 1];

            L.marker(startPoint, { icon: startIcon }).addTo(map).bindPopup("Start");

            L.marker(endPoint, { icon: finishIcon }).addTo(map).bindPopup("Finish");

            new Chart(document.getElementById("elevation-chart"), {
                type: "line",
                data: {
                    labels: distances,
                    datasets: [{
                        label: "Elevation (m)",
                        data: elevations,
                        borderWidth: 2,
                        tension: 0.2,
                        pointRadius: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: "Distance (km)"
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: "Elevation (m)"
                            }
                        }
                    }
                }
            });

        }

    } catch (error) {
        console.error("Error loading GPX:", error);
    }

});