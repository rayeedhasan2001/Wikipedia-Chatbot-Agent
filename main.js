document.getElementById('questionForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = document.getElementById('questionInput').value;
    const answerDiv = document.getElementById('answer');
    const answerText = document.getElementById('answerText');
    const sourcesList = document.getElementById('sourcesList');
    const loadingIndicator = document.getElementById('loadingIndicator');

    // Hide answer and show loading indicator
    answerDiv.classList.add('hidden');
    loadingIndicator.classList.remove('hidden');
    sourcesList.innerHTML = '';

    try {
        const response = await fetch('http://localhost:8000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        
        // Hide loading indicator and show answer
        loadingIndicator.classList.add('hidden');
        answerDiv.classList.remove('hidden');
        
        answerText.textContent = data.answer;

        sourcesList.innerHTML = ''; // Clear previous sources
        data.sources.forEach(source => {
            const li = document.createElement('li');
            li.textContent = source;
            sourcesList.appendChild(li);
        });
    } catch (error) {
        console.error('Error:', error);
        loadingIndicator.classList.add('hidden');
        answerDiv.classList.remove('hidden');
        answerText.textContent = 'An error occurred while fetching the answer.';
    }
});