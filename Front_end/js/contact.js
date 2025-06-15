const globe = Globe()(document.getElementById("globeViz"))
  .globeImageUrl('//unpkg.com/three-globe/example/img/earth-dark.jpg')
  .bumpImageUrl('//unpkg.com/three-globe/example/img/earth-topology.png')
  .backgroundImageUrl('//unpkg.com/three-globe/example/img/night-sky.png')
  .showAtmosphere(true)
  .atmosphereColor('#3a228a')
  .atmosphereAltitude(0.25)
  .labelsData([
    {
      lat: 47.3769,
      lng: 8.5417,
      text: 'Zürich',
      size: 1.5,
      color: 'red'
    }
  ])
  .labelLat(d => d.lat)
  .labelLng(d => d.lng)
  .labelText(d => d.text)
  .labelSize(d => d.size)
  .labelColor(d => d.color)
  .labelDotRadius(0.6)
  .onLabelClick(() => {
    document.getElementById("infoBox").style.display = "block";
  });

globe.controls().autoRotate = true;
globe.controls().autoRotateSpeed = 0.3;

// Wolken hinzufügen
const CLOUDS_IMG = '//unpkg.com/three-globe/example/img/fair_clouds_4k.png';
const cloudMaterial = new THREE.MeshLambertMaterial({
  map: new THREE.TextureLoader().load(CLOUDS_IMG),
  transparent: true
});

const CLOUDS_RADIUS = globe.getGlobeRadius() * 1.01;
const cloudSphere = new THREE.Mesh(
  new THREE.SphereGeometry(CLOUDS_RADIUS, 75, 75),
  cloudMaterial
);

globe.scene().add(cloudSphere);

(function animateClouds() {
  cloudSphere.rotation.y += 0.0003;
  requestAnimationFrame(animateClouds);
})();
