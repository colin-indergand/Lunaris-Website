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


// Beobachter, um zu prüfen, ob die Kacheln im Viewport erscheinen
const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Animation nur einmal starten
            animateValue("usersCount", 0, 123456, 2000);
            animateValue("marketCap", 0, 7453125124, 2500);
            animateValue("txTotal", 0, 12345678000, 3000);
            animateValue("tps", 0, 12320, 2000);

            observer.disconnect(); // Stoppt Beobachtung
        }
    });
}, { threshold: 0.5 });

// Starte Beobachtung beim Container (z. B. .data-grid)
observer.observe(document.querySelector(".data-grid"));

// Animationsfunktion
function animateValue(id, start, end, duration) {
    const obj = document.getElementById(id);
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        obj.textContent = Math.floor(progress * (end - start) + start).toLocaleString();
        if (progress < 1) {
            window.requestAnimationFrame(step);
        } else {
            obj.textContent = end.toLocaleString(); // Endwert setzen
        }
    };
    window.requestAnimationFrame(step);
}



// Daten Weltkarte

let countryData = [];

fetch(dataUrl)
  .then(res => res.json())
  .then(data => {
    countryData = data;
    am5.ready(function () {
      const root = am5.Root.new("mapdiv");
      root.setThemes([am5themes_Animated.new(root)]); 
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

      polygonSeries.mapPolygons.template.states.create("hover", {
        fill: am5.color(0x9966ff)
      });

      polygonSeries.mapPolygons.template.events.on("click", function(ev) {
        const country = ev.target.dataItem.dataContext;
        document.getElementById("countryInfoPanel").classList.remove("hidden");
        document.getElementById("countryName").innerText = country.name;

        const clickedISO = country.id;
        const match = countryData.find(item => item.iso2 === clickedISO);

        // Style für aktives Land
        polygonSeries.mapPolygons.template.states.create("active", {
          fill: am5.color(0xe0aaff) // hell-lila
        });

        document.getElementById("pop").innerText = match && match.population ? Number(match.population).toLocaleString() : "-";
        document.getElementById("gdp").innerText = match && match.gdp ? (match.gdp/1e9).toFixed(1) + " Mrd. USD" : "-";
        document.getElementById("inflation").innerText = match && match.inflation ? match.inflation.toFixed(2) + " %" : "-";
        document.getElementById("accounts").innerText = match && match.accounts ? match.accounts.toFixed(1) + " %" : "-";
        document.getElementById("unemployment").innerText = match && match.unemployment ? match.unemployment.toFixed(1) + " %" : "-";
      });

      // Klick außerhalb der Karte schließt das Info-Panel
      document.addEventListener("click", function (event) {
        const mapDiv = document.getElementById("mapdiv");
        const infoPanel = document.getElementById("countryInfoPanel");
        if (!mapDiv.contains(event.target)) {
          infoPanel.classList.add("hidden");
        }
      });
    });
  });

// Beispiel-Aufruf nach dem Laden:
window.addEventListener('DOMContentLoaded', () => {
  animateValue("usersCount", 0, 123456, 1800);
  animateValue("marketCap", 0, 7453125124, 2000);
  animateValue("txTotal", 0, 12345678000, 2200);
  animateValue("tps", 0, 12320, 1200);
});


