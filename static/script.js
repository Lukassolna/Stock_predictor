document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById('myButton').addEventListener('click', function() {
        document.getElementById('displayText').innerHTML = 'Button clicked!';
    });
});
