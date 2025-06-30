

am5.ready(function () {
  let root = am5.Root.new("globeChart");
  root.setThemes([am5themes_Animated.new(root)]);

  let chart = root.container.children.push(
    am5map.MapChart.new(root, {
      projection: am5map.geoOrthographic(),
      panX: "rotateX",
      panY: "rotateY",
      layout: root.verticalLayout
    })
  );

  let polygonSeries = chart.series.push(
    am5map.MapPolygonSeries.new(root, {
      geoJSON: am5geodata_worldLow,
      exclude: ["AQ"]
    })
  );

  polygonSeries.mapPolygons.template.setAll({
    tooltipText: "{name}",
    interactive: true,
    fill: am5.color(0x1b1133),
    stroke: am5.color(0x6600cc),
    strokeWidth: 0.7,
    strokeOpacity: 0.6  
  });

  let pointSeries = chart.series.push(
    am5map.MapPointSeries.new(root, {
      valueField: "value",
      calculateAggregates: true,
      longitudeField: "geometry.coordinates.0",
      latitudeField: "geometry.coordinates.1"
    })
  );

pointSeries.bullets.push(function (root, dataItem) {
    const circle = am5.Circle.new(root, {
        radius: 6,
        fill: am5.color(0xffffff),          // Weißer Punkt
        stroke: am5.color(0xaa00ff),        // Optionaler Rand
        strokeWidth: 1,
        tooltipText: "{title}",
        interactive: true,
        cursorOverStyle: "pointer"
    });

    // DEBUG: Klick testen
    circle.events.on("click", (event, d) => {
        const data = d;

        document.getElementById("popup-title").textContent = data.title;
        document.getElementById("popup-office").textContent = data.office;
        document.getElementById("popup-address").textContent = data.address;
        document.getElementById("popup-email").textContent = data.email;
        document.getElementById("popup-phone").textContent = data.phone;

        const popup = document.getElementById("popup");
        popup.classList.remove("hidden");
        popup.style.display = "block"; // Optional fallback
    });


    return am5.Bullet.new(root, { sprite: circle });
});


  const points = [
    {
      id: "zurich",
      title: "Zürich",
      geometry: { type: "Point", coordinates: [8.5417, 47.3769] },
      office: "Headquarter",
      address: "Bahnhofstrasse 1, 8001 Zürich, Schweiz",
      email: "info@lunaris.global",
      phone: "+41 44 123 45 67"
    },
    {
      id: "ny",
      title: "New York",
      geometry: { type: "Point", coordinates: [-74.006, 40.7128] },
      office: "US Office",
      address: "5th Avenue, New York, NY",
      email: "usa@lunaris.global",
      phone: "+1 212 123 4567"
    }
  ];
  pointSeries.data.setAll(points);

  // LINIE zwischen Zürich und New York (gewölbt)
  let lineSeries = chart.series.push(
    am5map.MapLineSeries.new(root, {
      geoJSON: undefined,
      stroke: am5.color(0xffffff),
      strokeWidth: 2,
      strokeOpacity: 0.4,
      greatCircle: true // <- macht die Linie gewölbt!
    })
  );

  lineSeries.data.setAll([
    {
      geometry: {
        type: "LineString",
        coordinates: [
          points[0].geometry.coordinates, // Zürich
          points[1].geometry.coordinates  // New York
        ]
      }
    }
  ]);

  // Popup schließen
  document.getElementById("popup-close").addEventListener("click", () => {
    document.getElementById("popup").classList.add("hidden");
  });

});