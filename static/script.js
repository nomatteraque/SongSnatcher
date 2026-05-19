document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('download-form');
    const urlInput = document.getElementById('url-input');
    const statusContainer = document.getElementById('status-container');
    const statusLabel = document.querySelector('.status-label');
    const dots = document.querySelector('.dots');
    const submitBtn = document.querySelector('.btn');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const url = urlInput.value.trim();
        if (!url) return;

        // Reset and show status
        statusContainer.classList.remove('hidden');
        statusLabel.classList.remove('error');
        statusLabel.textContent = 'Snatching payload';
        dots.classList.remove('static-dots');
        
        // Disable inputs
        submitBtn.disabled = true;
        urlInput.disabled = true;
        submitBtn.style.opacity = '0.5';

        try {
            const response = await fetch('/download', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url })
            });

            if (!response.ok) {
                let errorMsg = 'Connection sequence failed.';
                try {
                    const data = await response.json();
                    errorMsg = data.message || errorMsg;
                } catch(e) {}
                throw new Error(errorMsg);
            }

            const contentType = response.headers.get("content-type");
            if (contentType && contentType.indexOf("application/json") !== -1) {
                const data = await response.json();
                if (!data.success) {
                    throw new Error(data.message);
                }
            } else {
                const disposition = response.headers.get('Content-Disposition');
                let filename = 'download';
                if (disposition && disposition.indexOf('attachment') !== -1) {
                    const filenameRegex = /filename[^;=\n]*=((['"]).*?\2|[^;\n]*)/;
                    const matches = filenameRegex.exec(disposition);
                    if (matches != null && matches[1]) { 
                        filename = decodeURIComponent(matches[1].replace(/['"]/g, ''));
                    }
                }

                const blob = await response.blob();
                const downloadUrl = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.style.display = 'none';
                a.href = downloadUrl;
                a.download = filename;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(downloadUrl);

                dots.classList.add('static-dots');
                dots.textContent = '';
                statusLabel.textContent = 'Payload extracted successfully.';
                urlInput.value = '';
            }
        } catch (error) {
            dots.classList.add('static-dots');
            statusLabel.classList.add('error');
            statusLabel.textContent = 'Error: ' + error.message;
        } finally {
            // Re-enable inputs
            submitBtn.disabled = false;
            urlInput.disabled = false;
            submitBtn.style.opacity = '1';
            urlInput.focus();
        }
    });
});
