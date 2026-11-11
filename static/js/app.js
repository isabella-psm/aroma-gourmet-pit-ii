document.querySelectorAll('.filter').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.filter').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    document.querySelectorAll('.product-card').forEach((card) => {
      card.hidden = button.dataset.category !== 'todos' && card.dataset.category !== button.dataset.category;
    });
  });
});

document.querySelectorAll('[data-copy-target]').forEach((button) => {
  button.addEventListener('click', async () => {
    const code = document.getElementById(button.dataset.copyTarget).textContent.trim();
    try {
      await navigator.clipboard.writeText(code);
      button.textContent = 'Código copiado!';
    } catch {
      button.textContent = `Código: ${code}`;
    }
  });
});

document.querySelectorAll('[data-table-search]').forEach((input) => {
  input.addEventListener('input', () => {
    const query = input.value.toLowerCase().trim();
    document.querySelectorAll(`#${input.dataset.tableSearch} tbody tr`).forEach((row) => {
      row.hidden = !row.textContent.toLowerCase().includes(query);
    });
  });
});

document.querySelectorAll('[data-status-filter]').forEach((select) => {
  select.addEventListener('change', () => {
    document.querySelectorAll(`#${select.dataset.statusFilter} tbody tr`).forEach((row) => {
      row.hidden = Boolean(select.value) && row.dataset.status !== select.value;
    });
  });
});
