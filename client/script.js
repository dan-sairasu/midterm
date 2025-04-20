let allPackages = [];

function renderPackages(packages) {
  const container = document.getElementById('packages');
  container.innerHTML = '';

  if (packages.length === 0) {
    container.innerHTML = '<div class="text-center text-muted">No packages found.</div>';
    return;
  }

  packages.forEach(pkg => {
    const card = document.createElement('div');
    card.className = 'col-md-4 mb-4';

    card.innerHTML = `
      <div class="card shadow-sm h-100">
        <div class="card-body">
          <h5 class="card-title">${pkg.destination}</h5>
          <p class="card-text">Price: <strong>$${pkg.price}</strong></p>
          <p class="card-text">Duration: ${pkg.duration}</p>
        </div>
      </div>
    `;
    container.appendChild(card);
  });
}

fetch('http://localhost:5000/api/packages')
  .then(response => response.json())
  .then(data => {
    allPackages = data;
    renderPackages(allPackages);
  })
  .catch(error => {
    console.error('Error fetching packages:', error);
    document.getElementById('packages').innerHTML = `
      <div class="alert alert-danger" role="alert">
        Failed to load packages.
      </div>
    `;
  });

// Events
document.getElementById('filterType').addEventListener('change', switchFilterType);
document.getElementById('search').addEventListener('input', filterPackages);
document.getElementById('min').addEventListener('input', filterPackages);
document.getElementById('max').addEventListener('input', filterPackages);

// Toggle filter input mode
function switchFilterType() {
  const type = document.getElementById('filterType').value;
  const textInput = document.getElementById('textInputWrapper');
  const rangeInput = document.getElementById('rangeInputWrapper');

  if (type === 'price' || type === 'duration') {
    textInput.classList.add('d-none');
    rangeInput.classList.remove('d-none');
  } else {
    textInput.classList.remove('d-none');
    rangeInput.classList.add('d-none');
  }

  filterPackages();
}

function filterPackages() {
  const type = document.getElementById('filterType').value;
  let filtered = allPackages;

  if (type === 'price') {
    const min = parseFloat(document.getElementById('min').value) || 0;
    const max = parseFloat(document.getElementById('max').value) || Infinity;
    filtered = allPackages.filter(pkg => pkg.price >= min && pkg.price <= max);
  } else if (type === 'duration') {
    const min = parseFloat(document.getElementById('min').value) || 0;
    const max = parseFloat(document.getElementById('max').value) || Infinity;
    filtered = allPackages.filter(pkg => {
      const numDays = parseInt(pkg.duration); // assumes "5 days", "3", etc.
      return !isNaN(numDays) && numDays >= min && numDays <= max;
    });
  } else {
    const term = document.getElementById('search').value.toLowerCase();
    filtered = allPackages.filter(pkg =>
      pkg.destination.toLowerCase().includes(term)
    );
  }

  renderPackages(filtered);
}
