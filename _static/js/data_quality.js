// Save users browser data
const browser = navigator.userAgent;

function saveBrowserData() {
    document.getElementById('id_browser').value = browser;
}

document.addEventListener('DOMContentLoaded', function() {
    let page = window.location.href;

    let blur_data = localStorage.getItem('dictionary'); //retrieve 
    let myDictionary = JSON.parse(blur_data); // parse

    if (!myDictionary) { 
        // If it doesn't exist, create and save it
        console.log('creating')
        myDictionary = {
            page: 0,
          };
          localStorage.setItem('dictionary', JSON.stringify(myDictionary));
        }
        
});


count=0
// Event listener for blur event
window.addEventListener('blur', function() {
    // Code to save that the user clicked out of the window
    console.log('blur event detected in page:')
    count ++
    console.log(count)
    let page = window.location.href;

    let blur_data = localStorage.getItem('dictionary'); //retrieve 
    let myDictionary = JSON.parse(blur_data); // parse

    // Check if the 'page' key exists in the dictionary
    if (page in myDictionary) {
        // If yes, increment its value
        console.log('incrementing page')
        myDictionary[page]++;
    } else {
        // If not, set it to 0 (or any default value)
        console.log('setting page to 1')
        myDictionary[page] = 1;
    }

    // Save the updated dictionary back to localStorage
    localStorage.setItem('dictionary', JSON.stringify(myDictionary));

    // Use the updated dictionary as needed
    console.log(myDictionary);

    document.getElementById('id_blur_event_counts').value = JSON.stringify(myDictionary);
       

});

