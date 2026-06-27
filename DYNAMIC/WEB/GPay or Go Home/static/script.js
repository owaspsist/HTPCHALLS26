document.querySelectorAll('.purchase-form').forEach(form => {
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const terminal = document.getElementById('terminal-response');
        terminal.style.display = 'block';
        terminal.style.color = '#ffffff';
        terminal.innerHTML = '[*] Sending transaction data packet...';

        const formData = new FormData(form);

        try {
            const response = await fetch('/checkout', {
                method: 'POST',
                body: formData
            });
            
            const result = await response.json();
            
            if (result.success) {
                if (result.exploit) {
                    terminal.style.color = '#00ff66'; // Green on success
                    terminal.innerHTML = result.message;
                } else {
                    terminal.style.color = '#ffb300'; // Amber warning
                    terminal.innerHTML = `[!] Warning: ${result.message}`;
                }
            } else {
                terminal.style.color = '#ff3333'; // Red error
                terminal.innerHTML = `[-] Error: ${result.message}`;
            }
        } catch (error) {
            terminal.style.color = '#ff3333';
            terminal.innerHTML = '[-] Critical Network Error Connection Refused.';
        }
    });
});
