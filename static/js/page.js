document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("answerForm");
  const hidden = document.getElementById("answerHidden");
  if (!form || !hidden) return;

  let locked = false;

  document.querySelectorAll(".optBtn").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (locked) return;
      locked = true;

      // ✅ 어떤 선택지를 눌렀는지 hidden에 저장
      hidden.value = btn.dataset.val;

      // ✅ 페이드 아웃 후 submit
      document.body.classList.remove("fade-in");
      document.body.classList.add("fade-out");

      setTimeout(() => form.submit(), 170);
    });
  });
});