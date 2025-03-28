document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.querySelector('.file-input');
    const fileInfo = document.querySelector('.file-info');

    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            const fileName = e.target.files[0].name;
            const fileSize = (e.target.files[0].size / 1024 / 1024).toFixed(2);

            fileInfo.textContent = `Selected file: ${fileName} (${fileSize} MB)`;

            if (fileSize > 10) {
                fileInfo.textContent = 'File too large. Max 10MB allowed.';
                fileInfo.style.color = 'red';
                e.target.value = '';
            }
        }
    });
});