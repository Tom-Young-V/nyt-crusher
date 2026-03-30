// content.js
console.log("Content script loaded!");

// Listen for messages from the background script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === "getEntireHTML") {
        // Retrieve the entire HTML content
        const entireHTML = document.documentElement.outerHTML;
        console.log("Entire HTML content:", entireHTML);
    }
});
