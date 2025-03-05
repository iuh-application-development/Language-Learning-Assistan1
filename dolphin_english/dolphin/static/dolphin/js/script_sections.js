document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".section__header").forEach(function (header) {
        header.addEventListener("contextmenu", function (event) {
            event.preventDefault(); // Ngăn menu chuột phải mặc định

            const checkbox = this.previousElementSibling; // Lấy checkbox của section được click
            const allCheckboxes = document.querySelectorAll(".section__toggle"); // Lấy tất cả checkbox của các section

            // Kiểm tra nếu section được click đã mở hay chưa
            const isCurrentlyOpen = checkbox.checked;

            // Đóng tất cả các section trước khi mở mới
            allCheckboxes.forEach(cb => {
                cb.checked = false;
            });

            // Toggle trạng thái của section được click
            if (!isCurrentlyOpen) {
                checkbox.checked = true;
            }
        });
    });
});
