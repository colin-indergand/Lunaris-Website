function toggleMenu() {
  document.getElementById('nav').classList.toggle('open');
}

function switchLanguage(select) {
  const url = select.value;
  window.location.href = url;
}

function toggleMobileMenu() {
  const menu = document.getElementById('mobileMenu');
  menu.classList.toggle('open');
}


// Beispielhafte Platzhalter-Funktion
function showMore(sectionId) {
  const el = document.getElementById(sectionId);
  el.classList.toggle("expanded");
}

// JSON DATEN INTEGRIEREN
let populationData = [];

fetch("/static/world_population.json")
  .then(response => response.json())
  .then(data => {
    populationData = data;
  });


am5.ready(function () {
  const root = am5.Root.new("mapdiv");
  root.setThemes([am5.Theme.new(root)]);

  const chart = root.container.children.push(
    am5map.MapChart.new(root, {
      panX: "rotateX",
      panY: "none",
      projection: am5map.geoMercator()
    })
  );

  const polygonSeries = chart.series.push(
    am5map.MapPolygonSeries.new(root, {
      geoJSON: am5geodata_worldLow,
      exclude: ["AQ"]
    })
  );

  polygonSeries.mapPolygons.template.setAll({
    tooltipText: "{name}",
    interactive: true,
    fill: am5.color(0x222222),
    stroke: am5.color(0xffffff),
    strokeWidth: 0.8,
    strokeOpacity: 0.5
  });

  polygonSeries.mapPolygons.template.setAll({
    tooltipText: "{name}",
    interactive: true,
    fill: am5.color(0x222222),
    stroke: am5.color(0xffffff),
    strokeWidth: 0.8,
    strokeOpacity: 0.5
  });

  polygonSeries.mapPolygons.template.events.on("click", function(ev) {
    const country = ev.target.dataItem.dataContext;
    document.getElementById("countryInfoPanel").classList.remove("hidden");
    document.getElementById("countryName").innerText = country.name;

    const clickedCountry = ev.target.dataItem.dataContext.name;
    const clickedISO = ev.target.dataItem.dataContext.id; // 2-Buchstaben-Code

    const match = populationData.find(item => item.iso2 === clickedISO);
    const population = match ? match.population.toLocaleString() : "n. v.";

    // ...dann in dein Panel einfügen
    document.getElementById("pop").innerText = `${population} Einwohner`;

    // Beispielhafte Platzhalterdaten – hier mit echten Daten verknüpfen
    document.getElementById("pop").innerText = "xx Mio.";
    document.getElementById("inflation").innerText = "x.xx %";
    document.getElementById("gdp").innerText = "x.x B USD";
    document.getElementById("users").innerText = "2.1 Mio.";
    document.getElementById("volume").innerText = "0 CHF.";
    document.getElementById("partners").innerText = "0";
    document.getElementById("penetration").innerText = "0 %";
  });

  // Klick außerhalb der Karte schließt das Info-Panel
  document.addEventListener("click", function (event) {
    const mapDiv = document.getElementById("mapdiv");
    const infoPanel = document.getElementById("countryInfoPanel");

    if (!mapDiv.contains(event.target)) {
        infoPanel.classList.add("hidden");
    }
  });

  polygonSeries.mapPolygons.template.states.create("hover", {
    fill: am5.color(0x9966ff)  // Helllila Hover-Farbe
  }); 
});








