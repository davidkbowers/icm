const phaseDataEl = document.getElementById('phase-options-data');
const phaseOptions = phaseDataEl ? JSON.parse(phaseDataEl.textContent) : [];

function phaseDisplay(phase) {
    return phase.name ? `${phase.code} - ${phase.name}` : phase.code;
}

function getPhaseById(phaseId) {
    return phaseOptions.find((phase) => phase.id === phaseId) || null;
}

function findPhaseIdByCode(code) {
    const match = phaseOptions.find((phase) => phase.code.toLowerCase() === code.toLowerCase());
    return match ? match.id : (phaseOptions[0]?.id ?? null);
}

const defaultPhaseId = phaseOptions[0]?.id ?? null;

// State
const jobs = [
    { id: 'D25746.02.03006.P2A', desc: 'Concrete Labor', phaseId: findPhaseIdByCode('INT') },
    { id: 'D25746.02.03005.OTF', desc: 'Concrete Labor', phaseId: findPhaseIdByCode('OTF') },
    { id: 'D25726.01.06005', desc: 'Misc. Carpenter Labor', phaseId: findPhaseIdByCode('DECON') }
];

const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

// Time entries state structure:
// rowIdx_colIdx: { hours: number, type: string, modifier: string }
let timesheetData = {};

let activeCell = null; // { rowIdx, colIdx }

// DOM Elements
const tbody = document.getElementById('timesheet-body');
const totalsRow = document.getElementById('daily-totals-row');
const addJobBtn = document.getElementById('add-job-btn');
const modal = document.getElementById('entry-modal');
const closeModalBtn = document.getElementById('close-modal');
const clearEntryBtn = document.getElementById('clear-entry');
const saveEntryBtn = document.getElementById('save-entry');
const modalTitle = document.getElementById('modal-title');
const modalSubtitle = document.getElementById('modal-subtitle');
const hourSlider = document.getElementById('hour-slider');
const hoursDisplay = document.getElementById('hours-display');
const quickBtns = document.querySelectorAll('.btn-chip');
const modifierSelect = document.getElementById('modifier-select');

// Initialize Table
function renderTable() {
    tbody.innerHTML = '';

    jobs.forEach((job, rowIdx) => {
        const tr = document.createElement('tr');

        // Job Info Column
        const jobTd = document.createElement('td');
        jobTd.className = 'job-col';
        jobTd.innerHTML = `
            <div class="job-cell-content">
                <span class="job-id">${job.id}</span>
                <span class="job-desc">${job.desc}</span>
                <select class="phase-select" data-row="${rowIdx}" ${phaseOptions.length ? '' : 'disabled'}>
                    ${phaseOptions.length
                        ? phaseOptions
                            .map((phase) => `<option value="${phase.id}" ${phase.id === job.phaseId ? 'selected' : ''}>${phaseDisplay(phase)}</option>`)
                            .join('')
                        : '<option value="">No phases configured</option>'
                    }
                </select>
            </div>
        `;
        const phaseSelect = jobTd.querySelector('.phase-select');
        phaseSelect.addEventListener('change', (event) => {
            jobs[rowIdx].phaseId = Number.parseInt(event.target.value, 10) || null;
        });
        tr.appendChild(jobTd);

        // Day Columns
        let rowTotal = 0;
        days.forEach((day, colIdx) => {
            const td = document.createElement('td');
            td.className = 'day-cell';
            if (colIdx >= 5) td.classList.add('weekend');

            const cellKey = `${rowIdx}_${colIdx}`;
            const entry = timesheetData[cellKey];

            if (entry && entry.hours > 0) {
                rowTotal += entry.hours;
                td.innerHTML = `
                    <div class="entry-pill">
                        <span class="entry-hours">${entry.hours}h</span>
                        <span class="entry-type type-${entry.type.toLowerCase()}">${entry.type}${entry.modifier ? ' + ' + entry.modifier : ''}</span>
                    </div>
                `;
            } else {
                td.classList.add('empty');
                td.innerHTML = '<i class="fa-solid fa-plus" style="font-size:1.2rem; opacity:0; transition:0.2s"></i>';
                td.addEventListener('mouseenter', () => td.querySelector('i').style.opacity = 1);
                td.addEventListener('mouseleave', () => td.querySelector('i').style.opacity = 0);
            }

            td.addEventListener('click', () => openModal(rowIdx, colIdx, job, day));
            tr.appendChild(td);
        });

        // Row Total Column
        const totalTd = document.createElement('td');
        totalTd.innerHTML = `<strong>${rowTotal}h</strong>`;
        tr.appendChild(totalTd);

        tbody.appendChild(tr);
    });

    renderTotals();
}

function renderTotals() {
    totalsRow.innerHTML = '<td>Daily Totals:</td>';
    let grandTotal = 0;

    days.forEach((day, colIdx) => {
        let colTotal = 0;
        jobs.forEach((job, rowIdx) => {
            const entry = timesheetData[`${rowIdx}_${colIdx}`];
            if (entry) colTotal += entry.hours;
        });
        grandTotal += colTotal;
        const td = document.createElement('td');
        td.innerHTML = colTotal > 0 ? `${colTotal}h` : '-';
        totalsRow.appendChild(td);
    });

    const weekTotalTd = document.createElement('td');
    weekTotalTd.innerHTML = '<strong style="color:var(--accent)">' + `${grandTotal}h` + '</strong>';
    totalsRow.appendChild(weekTotalTd);
}

// Modal Logic
function openModal(rowIdx, colIdx, job, day) {
    activeCell = { rowIdx, colIdx };
    const cellKey = `${rowIdx}_${colIdx}`;
    const existing = timesheetData[cellKey];

    const phase = getPhaseById(job.phaseId);
    const phaseLabel = phase ? ` (${phaseDisplay(phase)})` : '';
    modalSubtitle.innerText = `${job.desc}${phaseLabel} - ${day}`;

    if (existing) {
        hourSlider.value = existing.hours;
        hoursDisplay.innerText = existing.hours;
        document.querySelector(`.type-radio input[value="${existing.type}"]`).checked = true;
        modifierSelect.value = existing.modifier || '';
    } else {
        hourSlider.value = 0;
        hoursDisplay.innerText = '0';
        document.querySelector('.type-radio input[value="ST"]').checked = true;
        modifierSelect.value = '';
    }

    modal.classList.add('active');
}

function closeModal() {
    modal.classList.remove('active');
    activeCell = null;
}

// Novel Input Interactions
hourSlider.addEventListener('input', (e) => {
    hoursDisplay.innerText = e.target.value;
});

quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const addVal = parseFloat(btn.getAttribute('data-val'));
        let current = parseFloat(hourSlider.value);
        let newVal = Math.min(24, current + addVal);
        hourSlider.value = newVal;
        hoursDisplay.innerText = newVal;
    });
});

saveEntryBtn.addEventListener('click', () => {
    if (!activeCell) return;

    const hours = parseFloat(hourSlider.value);
    const type = document.querySelector('.type-radio input:checked').value;
    const modifier = modifierSelect.value;
    const cellKey = `${activeCell.rowIdx}_${activeCell.colIdx}`;

    if (hours > 0) {
        timesheetData[cellKey] = { hours, type, modifier };
    } else {
        delete timesheetData[cellKey];
    }

    closeModal();
    renderTable();
    showToast();
});

clearEntryBtn.addEventListener('click', () => {
    if (!activeCell) return;
    const cellKey = `${activeCell.rowIdx}_${activeCell.colIdx}`;
    delete timesheetData[cellKey];
    closeModal();
    renderTable();
});

closeModalBtn.addEventListener('click', closeModal);
modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
});

addJobBtn.addEventListener('click', () => {
    const jobId = (window.prompt('Enter Job Number', '') || '').trim();
    if (!jobId) {
        return;
    }

    const category = (window.prompt('Enter Category', 'General Labor') || 'General Labor').trim();
    jobs.push({
        id: jobId,
        desc: category,
        phaseId: defaultPhaseId,
    });
    renderTable();
});

function showToast() {
    const toast = document.getElementById('toast');
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// Initialize Dummy Data to look alive
timesheetData = {
    '0_0': { hours: 8, type: 'ST', modifier: '' },
    '0_1': { hours: 8, type: 'ST', modifier: '' },
    '0_2': { hours: 8, type: 'ST', modifier: '' },
    '0_3': { hours: 8, type: 'ST', modifier: '' },
    '0_4': { hours: 8, type: 'ST', modifier: '' },
    '1_5': { hours: 4, type: 'OT', modifier: '' },
    '2_0': { hours: 2, type: 'ST', modifier: 'HZ/CS' }
};

// Start
renderTable();
