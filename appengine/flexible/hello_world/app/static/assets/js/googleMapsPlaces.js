function initMap() {
    console.log('initMap')
    const input = document.getElementById("user__address");
    const options = {
        componentRestrictions: { country: "mx" },
        // fields: ["formatted_address", "geometry", "name"],
        // strictBounds: false,
        // types: ["establishment"],
    };
    const autocomplete = new google.maps.places.Autocomplete(input, options);
    
    autocomplete.addListener("place_changed", () => {
        const place = autocomplete.getPlace();
    });
       
}