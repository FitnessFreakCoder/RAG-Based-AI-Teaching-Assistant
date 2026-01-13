const queryInput = document.getElementById('queryInput');
        const askButton = document.getElementById('askButton');
        const statusMessage = document.getElementById('statusMessage');
        const statusText = document.getElementById('statusText');
        const contextSection = document.getElementById('contextSection');
        const contextChunks = document.getElementById('contextChunks');
        const responseSection = document.getElementById('responseSection');
        const responseText = document.getElementById('responseText');

        // Example query click handlers
        document.querySelectorAll('.example-query').forEach(el => {
            el.addEventListener('click', () => {
                queryInput.value = el.dataset.query;
                queryInput.focus();
            });
        });

        // Enter key handler
        queryInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !askButton.disabled) {
                askQuestion();
            }
        });

        askButton.addEventListener('click', askQuestion);

        async function askQuestion() {
            const query = queryInput.value.trim();
            
            if (!query) {
                alert('Please enter a question');
                return;
            }

            // Reset UI
            askButton.disabled = true;
            statusMessage.classList.remove('hidden', 'error');
            statusMessage.classList.add('info');
            statusText.textContent = 'Processing your question...';
            contextSection.classList.add('hidden');
            responseSection.classList.add('hidden');
            contextChunks.innerHTML = '';
            responseText.textContent = '';

            try {
                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ query: query })
                });

                if (!response.ok) {
                    throw new Error('Failed to get response');
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder();
                let buffer = '';

                while (true) {
                    const { done, value } = await reader.read();
                    
                    if (done) break;

                    buffer += decoder.decode(value, { stream: true });
                    const lines = buffer.split('\n\n');
                    buffer = lines.pop();

                    for (const line of lines) {
                        if (line.startsWith('data: ')) {
                            const data = JSON.parse(line.slice(6));
                            
                            if (data.type === 'context') {
                                displayContext(data.chunks);
                                statusText.textContent = 'Generating answer...';
                            } else if (data.type === 'response') {
                                if (responseSection.classList.contains('hidden')) {
                                    responseSection.classList.remove('hidden');
                                }
                                responseText.textContent += data.text;
                            } else if (data.type === 'done') {
                                statusMessage.classList.remove('info');
                                statusMessage.classList.add('success');
                                statusText.textContent = '✓ Answer generated successfully!';
                                setTimeout(() => {
                                    statusMessage.classList.add('hidden');
                                }, 3000);
                            }
                        }
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                statusMessage.classList.remove('info');
                statusMessage.classList.add('error');
                statusText.textContent = '✗ Error: ' + error.message;
            } finally {
                askButton.disabled = false;
            }
        }

        function displayContext(chunks) {
            contextSection.classList.remove('hidden');
            contextChunks.innerHTML = '';

            chunks.forEach(chunk => {
                const chunkDiv = document.createElement('div');
                chunkDiv.className = 'context-chunk';
                chunkDiv.innerHTML = `
                    <div class="chunk-header">
                        <div class="chunk-title">${chunk.Title}</div>
                        <div class="chunk-time">${chunk.Start_HMS} - ${chunk.End_HMS}</div>
                    </div>
                    <div class="chunk-text">${chunk.Text}</div>
                `;
                contextChunks.appendChild(chunkDiv);
            });
        }

        // Check server health on load
        fetch('/health')
            .then(r => r.json())
            .then(data => {
                console.log('Server status:', data);
                if (data.ollama === 'disconnected') {
                    statusMessage.classList.remove('hidden');
                    statusMessage.classList.add('error');
                    statusText.textContent = '⚠️ Warning: Ollama server not connected';
                }
            })
            .catch(err => console.error('Health check failed:', err));