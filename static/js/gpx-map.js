document.addEventListener("DOMContentLoaded", async function () {

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

    function createStartIcon() {
        return new L.Icon({
            iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-green.png",
            shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
    }

    function createFinishIcon() {
        return new L.Icon({
            iconUrl: "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
            shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
    }

    async function loadGpxData(gpxUrl) {
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

        return {
            latlngs,
            distances,
            elevations,
            totalDistance,
            totalElevationGain
        };
    }

    function createBaseMap(element, interactive = true) {
        const map = L.map(element, {
            zoomControl: interactive,
            dragging: interactive,
            scrollWheelZoom: interactive,
            doubleClickZoom: interactive,
            boxZoom: interactive,
            keyboard: interactive,
            tap: interactive,
            touchZoom: interactive,
            attributionControl: true
        });

        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
            maxZoom: 18,
            attribution: "&copy; OpenStreetMap contributors"
        }).addTo(map);

        return map;
    }

    async function renderDetailPageMap() {
        const gpxScript = document.getElementById("gpx-url");
        const mapElement = document.getElementById("ride-map");

        if (!gpxScript || !mapElement) return;

        const gpxUrl = JSON.parse(gpxScript.textContent);
        const map = createBaseMap(mapElement, true);

        const startIcon = createStartIcon();
        const finishIcon = createFinishIcon();

        try {
            const data = await loadGpxData(gpxUrl);

            if (data.latlngs.length > 0) {
                const distanceElement = document.getElementById("ride-distance");
                const elevationElement = document.getElementById("ride-elevation");

                if (distanceElement) {
                    distanceElement.textContent = data.totalDistance.toFixed(1);
                }

                if (elevationElement) {
                    elevationElement.textContent = Math.round(data.totalElevationGain);
                }

                const polyline = L.polyline(data.latlngs, {
                    color: "#e63946",
                    weight: 5,
                    opacity: 0.8
                }).addTo(map);

                map.fitBounds(polyline.getBounds());

                const startPoint = data.latlngs[0];
                const endPoint = data.latlngs[data.latlngs.length - 1];

                L.marker(startPoint, { icon: startIcon }).addTo(map).bindPopup("Start");
                L.marker(endPoint, { icon: finishIcon }).addTo(map).bindPopup("Finish");

                const chartElement = document.getElementById("elevation-chart");

                if (chartElement) {
                    new Chart(chartElement, {
                        type: "line",
                        data: {
                            labels: data.distances,
                            datasets: [{
                                label: "Elevation (m)",
                                data: data.elevations,
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
            }
        } catch (error) {
            console.error("Error loading detail GPX:", error);
        }
    }

    async function renderListPageMaps() {
        const mapElements = document.querySelectorAll(".ride-map");
        if (!mapElements.length) return;

        for (const mapElement of mapElements) {
            const gpxUrl = mapElement.dataset.gpxUrl;
            if (!gpxUrl) continue;

            const map = createBaseMap(mapElement, false);

            try {
                const data = await loadGpxData(gpxUrl);

                if (data.latlngs.length > 0) {
                    const polyline = L.polyline(data.latlngs, {
                        color: "#e63946",
                        weight: 4,
                        opacity: 0.8
                    }).addTo(map);

                    map.fitBounds(polyline.getBounds());
                }
            } catch (error) {
                console.error("Error loading list GPX:", error);
            }
        }
    }

    await renderDetailPageMap();
    await renderListPageMaps();
});