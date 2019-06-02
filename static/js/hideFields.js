function hideFields() {
    // Hide Definition
    if (hd.checked) {
        console.log('Hiding definition.')
        hideDefinition()
        showWord()
    }

    // Hide Spelling
    if (hs.checked) {
        console.log('Hiding spelling.')
        showDefinition()
        hideWord()
    }

    // Show all fields
    if (hn.checked) {
        showWord()
        showDefinition()
    }

}