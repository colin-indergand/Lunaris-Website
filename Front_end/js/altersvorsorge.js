
///////////////////////////////////////
// EINKOMMEN
//////////////////////////////////////

// Einkommen: Zeilen hinzufügen
function addIncomeBlock() {
  const container = document.getElementById('income_blocks');
  const template = document.getElementById('income-entry-template');
  const clone = template.content.cloneNode(true);

  createDropdown(clone.querySelector('#select_income_start_age'), 1, 100);
  createDropdown(clone.querySelector('#select_income_end_age'), 1, 100);

  container.appendChild(clone);
  addBvgContribField();
}

// Einkommen: Zeilen entfernen

function removeIncomeBlock() {
  const container = document.getElementById('income_blocks');
  const tempEntries = container.querySelectorAll('.select-income-entry');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}

// Einkommen: Vermögenszeile ausblenden
function toggleVermoegen(selectElement) {
  const block = selectElement.closest('.income-entry, .select-income-entry');
  const period = block.querySelector('.select_income_vermögen_data');

  const show = selectElement.value === 'income_status_nicht_erwerbstätig';

  if (period) {
    period.style.display = show ? 'block' : 'none';
  }
}


///////////////////////////////////////
// BEITRAGSJAHRE
//////////////////////////////////////

// Beitragsjahre: Zeilen hinzufügen
function addContribYears() {
  const container = document.getElementById('contrib_gap_years');
  const contrib_gap = document.getElementById('contrib_gap_total_years');

  const gapValue = parseInt(contrib_gap.value);
  if (gapValue > 0) {
    const template = document.getElementById('contrib_gap_entry_template');
    const clone = template.content.cloneNode(true);

    const startSelect = clone.querySelector('.select-contrib-gap-start-age');
    const endSelect = clone.querySelector('.select-contrib-gap-end-age');

    createDropdown(startSelect, 1, 100);
    createDropdown(endSelect, 1, 100);

    container.appendChild(clone);
  } else {
    alert("Bitte zuerst eine Anzahl von Beitragslücken auswählen. (min. 1)");
  }
}

// Beitragsjahre: Elemente einblenden
function toggleContribData(selectElement) {
  const entry = document.getElementById('contrib_gap_years');
  const period = entry.querySelectorAll('.contrib-gap-period');

  const add_button = document.querySelector('.contrib-gap-add-button');
  const remove_button = document.querySelector('.contrib-gap-remove-button');

  const show = parseInt(selectElement.value) > 0;
  
  period.forEach (periods=> {
    periods.style.display = show ? 'inline' : 'none';
  });

  add_button.style.display = show ? 'inline' : 'none';
  remove_button.style.display = show ? 'inline' : 'none';
}

// Beitragsjahre: Zeilen entfernen

function removeContribYears() {
  const container = document.getElementById('contrib_gap_years');
  const tempEntries = container.querySelectorAll('.contrib-gap-period');

  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  }
}

///////////////////////////////////////
// VERHEIRATET / LEDIG
//////////////////////////////////////

// Yearly-Status: Zeilen hinzufügen
function addYearlyStatus() {
  const container = document.getElementById('yearly_status_data');
  const template = document.getElementById('yearly-status-data-template');
  const clone = template.content.cloneNode(true);

  createDropdown(clone.querySelector('#yearly_status_data_start_age'), 1, 100);
  createDropdown(clone.querySelector('#yearly_status_data_end_age'), 1, 100);

  container.appendChild(clone);
}

// Yearly-Status: Zeilen entfernen

function removeYearlyStatus() {
  const container = document.getElementById('yearly_status_data');
  const tempEntries = container.querySelectorAll('.select-entry-yearly-status');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}

///////////////////////////////////////
// ERZIEHUNGSGUTSCHRIFTEN
//////////////////////////////////////

// Childcare Credits: Kinder Jahrgang hinzufügen
function createChildcareVintage(selectElement) {
  const count = parseInt(selectElement.value);
  const container = document.getElementById('child_year_block');
  const template = document.querySelector('.child-template');

  container.querySelectorAll('.childcare-entry').forEach(e => e.remove());

  for (let i = 0; i < count; i++) {
    const clone = template.content.cloneNode(true);
    const entry = clone.querySelector('.childcare-entry');
    const label = clone.querySelector('label');
    const dropdown = clone.querySelector('.vintage-children');

    if (entry) entry.style.display = 'block';

    if (label) {
      label.textContent = `Geburtsjahr des ${i + 1}. Kindes`;
    }

    if (dropdown) {
      createDropdown(dropdown, 1900, 2025);
    }

    container.appendChild(clone);
  }
}

// Childcare Credits: Zeilen einblenden

function toggleChildcareCredits(selectElement) {  
  const block = document.getElementById('childcare_credits_data');
  const label_1 = block.querySelector('#children_count_block');
  const label_2 = block.querySelector('#child_year_block');

  const show = selectElement.value === 'Ja';

  label_1.style.display = show ? 'block' : 'none';
  label_2.style.display = show ? 'block' : 'none';

  const erziehungsBlock = document.getElementById('block_erziehunsgberechtigt');
  if (erziehungsBlock) erziehungsBlock.style.display = show ? 'block' : 'none';
  
  const dropdown = block.querySelector('.select-num-children-childcare-credits');
  const oldValue = dropdown.value

  if (show) {
    createDropdown(dropdown, 1, 50);
    if (oldValue && dropdown.querySelector(`option[value="${oldValue}"]`)) {
      dropdown.value = oldValue;    
    }
    // Automatisch Template erzeugen, wenn Wert gesetzt
    if (parseInt(dropdown.value) > 0) {
      createChildcareResponsibilityTemplates(dropdown);
    }
  }
}

//ERZIEHUNGSBERECHTIGUNG

function createChildcareResponsibilityTemplates(selectElement) {
  const count = parseInt(selectElement.value);
  const container = document.getElementById('block_erziehunsgberechtigt');
  const template = document.querySelector('.erziehungsberechtigt-template');

  // Entferne alle bisherigen Wrapper
  container.querySelectorAll('.erziehungsberechtigt-template-wrapper').forEach(e => e.remove());

  // Für jedes Kind einen Block erzeugen (auch bei count == 1)
  for (let i = 0; i < count; i++) {
    const clone = template.content.cloneNode(true);
    const toggler = clone.querySelector('.is-erziehungsberechtigt');
    const label = clone.querySelector('label');
    if (label) {
      label.textContent = `Durchgehend Erziehungsberechtigt für ${i + 1}. Kind`;
    }
    if (toggler) {
      toggler.value = "Ja";
      toggler.addEventListener('change', function() {
        toggleErziehungsberechtigt(this);
        toggleErziehungsberechtigtBeide(this);
      });
      toggleErziehungsberechtigt(toggler);
      toggleErziehungsberechtigtBeide(toggler);
    }
    const wrapper = clone.querySelector('.erziehungsberechtigt-template-wrapper');
    if (wrapper) wrapper.setAttribute('data-child', i);

    container.appendChild(clone);
  }
}


// Erziehungsberechtigt: Einzelne Zeilen einblenden
function toggleErziehungsberechtigt(selectElement) {
  const block = selectElement.closest('.erziehungsberechtigt-template-wrapper');
  const container = block.querySelector('.duration-erziehunsgberechtigt-standard');
  const add_button = block.querySelector('.erziehungsberechtigt-add-button');
  const remove_button = block.querySelector('.erziehungsberechtigt-remove-button');

  const show = selectElement.value === 'Nein';

  container.style.display = show ? 'block' : 'none';
  add_button.style.display = show ? 'inline' : 'none';
  remove_button.style.display = show ? 'inline' : 'none';

  const Dropdown_start = block.querySelector('.select-erziehungsberechtigt-start-age');
  const Dropdown_end = block.querySelector('.select-erziehungsberechtigt-end-age');

  const tempEntries = block.querySelectorAll('.erziehungsberechtigt-standard-temp');
  tempEntries.forEach(entry => {
    entry.style.display = show ? 'block' : 'none';
  });

  if (show) {
    createDropdown(Dropdown_start, 1900, 2025);
    createDropdown(Dropdown_end, 1900, 2025);
  }
}

// Erziehunsgberechtigt: Status einblenden
function toggleErziehungsberechtigtBeide(selectElement) {
  const block = selectElement.closest('.erziehungsberechtigt-template-wrapper');
  const container = block.querySelector('.status-erziehungsberechtigt-standard');

  const show = selectElement.value === 'Ja';


  if (container) {
    container.style.display = show ? 'block' : 'none';
  }
}

function addErziehungsberechtigt(buttonElement) {
    const wrapper = buttonElement.closest('.erziehungsberechtigt-template-wrapper');
    const container = wrapper.querySelector('.erziehungsberechtigt-standard');
    const template = wrapper.querySelector('.erziehungsberechtigt-standard-template');

    const childIndex = wrapper.getAttribute('data-child'); // ← Kind-Index abrufen

    const clone = template.content.cloneNode(true);

    const startAge = clone.querySelector('.select-erziehungsberechtigt-start-age-temp');
    const endAge = clone.querySelector('.select-erziehungsberechtigt-end-age-temp');
    const status = clone.querySelector('.select-erziehungsberechtigt-status-temp');

    if (startAge) startAge.setAttribute('name', `return-erziehungsberechtigt-start-age-${childIndex}[]`);
    if (endAge) endAge.setAttribute('name', `return-erziehungsberechtigt-end-age-${childIndex}[]`);
    if (status) status.setAttribute('name', `return-erziehungsberechtigt-status-${childIndex}[]`);

    // Optional: Label anpassen
    const labelStart = clone.querySelector('.erziehungsberechtigt-start-age-temp');
    if (labelStart && childIndex !== null) {
        labelStart.textContent = `Von Jahr:`;
    }
    const labelEnd = clone.querySelector('.erziehungsberechtigt-end-age-temp');
    if (labelEnd && childIndex !== null) {
        labelEnd.textContent = `Bis Jahr:`;
    }

    // Dropdowns befüllen
    createDropdown(startAge, 1900, 2025);
    createDropdown(endAge, 1900, 2025);

    // Wrapper für den Eintrag
    const cloneWrapper = document.createElement('div');
    cloneWrapper.classList.add('erziehungsberechtigt-standard-temp');
    cloneWrapper.appendChild(clone);

    // Eintrag anhängen
    container.appendChild(cloneWrapper);
}


// Erziehunsgberechtigt: Einzelne Zeilen entfernen

function removeErziehungsberechtigt(buttonElement) {
  const wrapper = buttonElement.closest('.erziehungsberechtigt-template-wrapper');
  const container = wrapper.querySelector('.erziehungsberechtigt-standard');
  const tempEntries = container.querySelectorAll('.erziehungsberechtigt-standard-temp');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}


///////////////////////////////////////
// BETREUUNGSGUTSCHRFITEN
//////////////////////////////////////

// Betreuungsgutschriften einblenden
function toggleBetreuungsgutschriften(selectElement) {
  const entry = selectElement.closest('.betreuungsgutschriften');

  const entries_container = entry.querySelector('#betreuungsgutschriften_container');
  const add_button = entry.querySelector('#betreuungsgutschriften_add_button');
  const remove_button = entry.querySelector('#betreuungsgutschriften_remove_button');

  const show = selectElement.value === 'Ja';

  entries_container.style.display = show ? 'block' : 'none';
  add_button.style.display = show ? 'inline' : 'none';
  remove_button.style.display = show ? 'inline' : 'none';

  const dropdown_1 = entry.querySelector('.select-start-year-betreuungsgutschriften');
  const dropdown_2 = entry.querySelector('.select-end-year-betreuungsgutschriften');

  if (show) {
    createDropdown(dropdown_1, 1900, 2025);
    createDropdown(dropdown_2, 1900, 2025);
  }
}

// Betreuungsgutschrfiten Blöcke hinzufügen
function addBetreuungsgutschriften() {
  const container = document.getElementById('betreuungsgutschriften_container');
  const template = document.getElementById('betreuungsgutschriften_container_template');

  const cloneWrapper = document.createElement('div');
  cloneWrapper.classList.add('betreuungsgutschriften-container-template');

  const clone = template.content.cloneNode(true);

  const Dropdown_start = clone.querySelector('.select-start-year-betreuungsgutschriften-temp');
  const Dropdown_end = clone.querySelector('.select-end-year-betreuungsgutschriften-temp');

  createDropdown(Dropdown_start, 1900, 2025);
  createDropdown(Dropdown_end, 1900, 2025);
  
  cloneWrapper.appendChild(clone);
  container.appendChild(cloneWrapper);
}

// Betreuungsgutschrfiten Blöcke entfernen

function removeBetreuungsgutschriften() {
  const container = document.getElementById('betreuungsgutschriften_container');
  const tempEntries = document.getElementsByClassName('betreuungsgutschriften-container-template');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}

///////////////////////////////////////
// BVG BEITRÄGE
//////////////////////////////////////

// BVG-Contrib: Angestellt / Selbständig einblenden
function addBvgContribField() {
  const dropdown = document.querySelectorAll('.income_select');

  let hasAngestellt = false;
  let hasSelbständig = false;

  dropdown.forEach(dropdown_all => {
    const value = dropdown_all.value;
    if (value === 'income_status_angestellt') hasAngestellt = true;
    if (value === 'income_status_selbständig') hasSelbständig = true;
  });

  const angestellt = document.getElementById('bvg_contrib_angestellt_container');
  const selbständig = document.getElementById('bvg_contrib_selbständig_container');

  angestellt.style.display = hasAngestellt ? 'block' : 'none';
  selbständig.style.display = hasSelbständig ? 'block' : 'none';
}

// BVG-Contrib: Angestellt einblenden
function toggleBvgcontribangestellt(selectElement) {
  const period = document.getElementById('bvg_contrib_angestellt_inputs');
  const add_button = document.getElementById('add_bvg_contrib_angest');
  const remove_button = document.getElementById('remove_bvg_contrib_angest');

  const show = selectElement.value === 'Ja';

  period.style.display = show ? 'block' : 'none';
  add_button.style.display = show ? 'inline' : 'none';
  remove_button.style.display = show ? 'inline' : 'none';

  const Dropdown_start = period.querySelector('.select-bvg-contrib-angestellt-start-age');
  const Dropdown_end = period.querySelector('.select-bvg-contrib-angestellt-end-age');

  if (show) {
    createDropdown(Dropdown_start, 1, 100);
    createDropdown(Dropdown_end, 1, 100);
  }
}

// BVG-Contrib: Selbständig einblenden
function toggleBvgcontribselbständig(selectElement) {
  const period = document.getElementById('bvg_contrib_selbständig_inputs');
  const add_button = document.getElementById('add_bvg_contrib_selbst');
  const remove_button = document.getElementById('remove_bvg_contrib_selbst');

  const show = selectElement.value === 'Ja';

  period.style.display = show ? 'block' : 'none';
  add_button.style.display = show ? 'inline' : 'none';
  remove_button.style.display = show ? 'inline' : 'none';

  const Dropdown_start = period.querySelector('.select-bvg-contrib-selbständig-start-age');
  const Dropdown_end = period.querySelector('.select-bvg-contrib-selbständig-end-age');

  if (!show) {
    document.querySelector('.select-bvg-contrib-selbständig-start-age').innerHTML = ''; 
    document.querySelector('.select-bvg-contrib-selbständig-end-age').innerHTML = '';    
  }  
  
  if (show) {
    createDropdown(Dropdown_start, 1, 100);
    createDropdown(Dropdown_end, 1, 100);
  }
}

// BVG-Contrib: Angestellt hinzufügen
function addBvgcontribangestellt() {
  const container = document.getElementById('bvg_contrib_angestellt_inputs');
  const template = document.getElementById('bvg_contrib_angestellt_template');

  const cloneWrapper = document.createElement('div');
  cloneWrapper.classList.add('bvg-contrib-entry-angestellt');

  const clone = template.content.cloneNode(true);

  const Dropdown_start = clone.querySelector('.select-bvg-contrib-angestellt-start-age-temp');
  const Dropdown_end = clone.querySelector('.select-bvg-contrib-angestellt-end-age-temp');

  createDropdown(Dropdown_start, 1, 100);
  createDropdown(Dropdown_end, 1, 100);
  
  cloneWrapper.appendChild(clone);
  container.appendChild(cloneWrapper);
}

// BVG-Contrib: Angestellt entfernen

function removeBvgcontribangestellt() {
  const container = document.getElementById('bvg_contrib_angestellt_inputs');
  const tempEntries = document.getElementsByClassName('bvg-contrib-entry-angestellt');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}

// BVG-Contrib: Selbständig hinzufügen
function addBvgcontribselbständig() {
  const container = document.getElementById('bvg_contrib_selbständig_inputs');
  const template = document.getElementById('bvg_contrib_selbständig_template');

  const cloneWrapper = document.createElement('div');
  cloneWrapper.classList.add('bvg-contrib-entry-selbständig');

  const clone = template.content.cloneNode(true);
  
  const Dropdown_start = clone.querySelector('.select-bvg-contrib-selbständig-start-age-temp');
  const Dropdown_end = clone.querySelector('.select-bvg-contrib-selbständig-end-age-temp');

  createDropdown(Dropdown_start, 1, 100);
  createDropdown(Dropdown_end, 1, 100);

  cloneWrapper.appendChild(clone);
  container.appendChild(cloneWrapper);
}

// BVG-Contrib: Selbständig entfernen

function removeBvgcontribselbständig() {
  const container = document.getElementById('bvg_contrib_selbständig_inputs');
  const tempEntries = document.getElementsByClassName('bvg-contrib-entry-selbständig');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}

///////////////////////////////////////
// ZINSSATZ
//////////////////////////////////////

// Yearly-Yield: Zeilen hinzufügen
function addYield() {
  const container = document.getElementById('bvg_yield');
  const template = document.getElementById('bvg_yield_template');
  const clone = template.content.cloneNode(true);

  createDropdown(clone.querySelector('#select_bvg_yield_start_age'), 1, 100);
  createDropdown(clone.querySelector('#select_bvg_yield_end_age'), 1, 100);
  createDropdown(clone.querySelector('#select_bvg_yield_yield'), 0.00, 100.00, 0.01);

  container.appendChild(clone);
}

// Yearly-Yield: Zeilen entfernen

function removeYield() {
  const container = document.getElementById('bvg_yield');
  const tempEntries = container.querySelectorAll('.bvg-yield-template');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}

///////////////////////////////////////
// CONTRIB AUFTEILUNG
//////////////////////////////////////

// BVG-Contrib-Share: Zeilen hinzufügen
function addContribShare() {
  const container = document.getElementById('bvg_contrib_share');
  const template = document.getElementById('bvg_contrib_share_template');
  const clone = template.content.cloneNode(true);

  createDropdown(clone.querySelector('#select_bvg_contrib_share_start_age'), 1, 100);
  createDropdown(clone.querySelector('#select_bvg_contrib_share_end_age'), 1, 100);
  createDropdown(clone.querySelector('#select_bvg_contrib_share_percentage'), 0, 100);

  container.appendChild(clone);
}

// BVG-Contrib-Share: Zeilen entfernen

function removeContribShare() {
  const container = document.getElementById('bvg_contrib_share');
  const tempEntries = container.querySelectorAll('.bvg-contrib-share-template');
 
  if (tempEntries.length > 0) {
    const last = tempEntries[tempEntries.length - 1];
    container.removeChild(last);
  } 
}


///////////////////////////////////////
// Monthly Pension Payment
//////////////////////////////////////

function toggleMonthlyPayment(selectElement) {
  const container = document.getElementById('monthly_pension');

  const show = selectElement.value == 'beliebig';

  container.style.display = show ? 'block' : 'none';
}


///////////////////////////////////////
// SPARRATE
//////////////////////////////////////

// Saving Rate: Elemente einblenden
function toggleSavingRate(selectElement) {
  const period = document.getElementById('saving_rate_range');

  const show = selectElement.value === 'Nein';

  period.style.display = show ? 'block' : 'none';
  if (show) {
    createDropdown('saving_rate_start_age', 1, 100);
    createDropdown('saving_rate_end_age', 1, 100);
  }
}


///////////////////////////////////////
// DROPDOWN ERSTELLEN
//////////////////////////////////////

// Funktion um Dropdowns zu erstellen
function createDropdown(idOrElement, min, max, step = 1) {
  const dropdown = typeof idOrElement === 'string'
      ? document.getElementById(idOrElement)
      : idOrElement;
  dropdown.innerHTML = '';
  for (let i = min; i <= max; i += step) {
      const option = document.createElement('option');
      option.value = i;
      option.textContent = (step < 1 ? i.toFixed(2) : i);
      dropdown.appendChild(option);
  }
}

document.querySelector('button[type="reset"]').addEventListener('click', function (e) {
    e.preventDefault(); // Verhindert das Standard-Reset-Verhalten

    // 1. Formular zurücksetzen (setzt alle Werte zurück)
    const form = document.querySelector('form');
    form.reset();

    // 2. Dynamisch hinzugefügte Blöcke entfernen
    // Einkommen
    document.querySelectorAll('.select-income-entry').forEach(e => e.remove());
    // Beitragslücken
    document.querySelectorAll('.contrib-gap-period').forEach(e => {
        if (!e.closest('#contrib_gap_period_container')) e.remove();
    });
    // Partner-Jahresstatus
    document.querySelectorAll('.select-entry-yearly-status').forEach(e => e.remove());
    // Erziehungsgutschriften
    document.querySelectorAll('.erziehungsberechtigt-template-wrapper').forEach((e, i) => { if (i > 0) e.remove(); });
    document.querySelectorAll('.erziehungsberechtigt-standard-temp').forEach(e => e.remove());
    // Betreuungsgutschriften
    document.querySelectorAll('.betreuungsgutschriften-container-template').forEach(e => e.remove());
    // BVG-Angestellt
    document.querySelectorAll('.bvg-contrib-entry-angestellt').forEach(e => e.remove());
    // BVG-Selbstständig
    document.querySelectorAll('.bvg-contrib-entry-selbständig').forEach(e => e.remove());
    // BVG-Zins
    document.querySelectorAll('.bvg-yield-template').forEach(e => e.remove());
    // BVG-Beitragssätze
    document.querySelectorAll('.bvg-contrib-share-template').forEach(e => e.remove());

  

    // 3. Alle Container/Bereiche wieder ausblenden
    [
        '#children_count_block',
        '#child_year_block',
        '#block_erziehunsgberechtigt',
        '#betreuungsgutschriften_container',
        '#contrib_gap_period_container',
        '#bvg_contrib_angestellt_container',
        '#bvg_contrib_angestellt_inputs',
        '#bvg_contrib_selbständig_container',
        '#bvg_contrib_selbständig_inputs',
        '#monthly_pension',
        '#saving_rate_range'
    ].forEach(selector => {
        const el = document.querySelector(selector);
        if (el) el.style.display = 'none';
    });

    // 4. Buttons wieder ausblenden
    document.querySelectorAll('button').forEach(btn => {
        if (
            btn.classList.contains('contrib-gap-add-button') ||
            btn.classList.contains('contrib-gap-remove-button') ||
            btn.classList.contains('erziehungsberechtigt-add-button') ||
            btn.classList.contains('erziehungsberechtigt-remove-button') ||
            btn.id === 'betreuungsgutschriften_add_button' ||
            btn.id === 'betreuungsgutschriften_remove_button' ||
            btn.id === 'add_bvg_contrib_angest' ||
            btn.id === 'remove_bvg_contrib_angest' ||
            btn.id === 'add_bvg_contrib_selbst' ||
            btn.id === 'remove_bvg_contrib_selbst'
        ) {
            btn.style.display = 'none';
        }
    });

    addBvgContribField();
});


document.getElementById("form").addEventListener("submit", async function (e) {
    e.preventDefault(); // Verhindert den Reload

    const form = e.target;
    const formData = new FormData(form);

    const response = await fetch("/altersvorsorge", {
        method: "POST",
        body: formData,
        headers: {
            "X-Requested-With": "XMLHttpRequest"  // zur Unterscheidung im Backend
        }
    });

    if (response.ok) {
        const html = await response.text();
        document.getElementById("results_section").innerHTML = html;
        document.getElementById("results_section").style.display = "block";
    } else {
        alert("Fehler beim Absenden.");
    }
});


function toggleInfoBox(icon) {
  // Schließe alle anderen Info-Boxen
  document.querySelectorAll('.info-icon.active').forEach(function(el) {
    if (el !== icon) el.classList.remove('active');
  });
  // Toggle aktuelle Box
  icon.classList.toggle('active');
}

// Optional: Schließen beim Klick außerhalb
document.addEventListener('click', function(e) {
  if (!e.target.classList.contains('info-icon')) {
    document.querySelectorAll('.info-icon.active').forEach(function(el) {
      el.classList.remove('active');
    });
  }
});



// Ausführung und Hinzufügen von Dropdowns
window.addEventListener('DOMContentLoaded', () => {
  createDropdown('vintage_vintage', 1900, 2025);
  createDropdown('income_start_age', 1, 100);
  createDropdown('income_end_age', 1, 100);
  createDropdown('contrib_gap_total_years', 0, 100);
  createDropdown('contrib_gap_start_age', 1, 100);
  createDropdown('contrib_gap_end_age', 1, 100);
  createDropdown('yearly-status-data-start-age', 1, 100);
  createDropdown('yearly-status-data-end-age', 1, 100);
  createDropdown('bvg_yield_start_age', 1, 100);
  createDropdown('bvg_yield_end_age', 1, 100);
  createDropdown('bvg_yield_yield', 0.00, 100.00, 0.01);
  createDropdown('bvg_contrib_share_start_age', 1, 100);
  createDropdown('bvg_contrib_share_end_age', 1, 100);
  createDropdown('bvg_contrib_share_percentage', 0, 100);

  const statusDropdowns = document.querySelectorAll('.income_select');
  statusDropdowns.forEach(dropdown => {
    addBvgContribField(dropdown);
    toggleVermoegen(dropdown);
  }); 

  const bvgAngestelltDropdowns = document.querySelectorAll('.select-bvg-contrib-angestellt');
  bvgAngestelltDropdowns.forEach(dropdown => {
    toggleBvgcontribangestellt(dropdown);
  });

  const bvgSelbstDropdowns = document.querySelectorAll('.select-bvg-contrib-selbständig');
  bvgSelbstDropdowns.forEach(dropdown => {
    toggleBvgcontribselbständig(dropdown);
  });

  const hasChildren = document.getElementById('has_children');
  const childrenCount = document.getElementById('amount_children_childcare_credits');
  if (hasChildren && childrenCount && hasChildren.value === 'Ja' && parseInt(childrenCount.value) > 0) {
    createChildcareResponsibilityTemplates(childrenCount);
  }

});

