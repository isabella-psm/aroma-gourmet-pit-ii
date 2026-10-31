document.querySelectorAll('.filter').forEach((button) => {
  button.addEventListener('click', () => {
    document.querySelectorAll('.filter').forEach((item) => item.classList.remove('active'));
    button.classList.add('active');
    document.querySelectorAll('.product-card').forEach((card) => {
      card.hidden = button.dataset.category !== 'todos' && card.dataset.category !== button.dataset.category;
    });
  });
});
