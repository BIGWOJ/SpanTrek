var simplemaps_countrymap_mapdata = {
    main_settings: {
        //General settings
        width: "responsive", //'700' or 'responsive'
        height: "800",
        background_transparent: "yes",
        border_color: "#ffa51f",

        //State defaults
        state_url: "",
        border_size: 1.5,
        all_states_inactive: "no",
        all_states_zoomable: "yes",

        //Location defaults
        location_description: "Location description",
        location_url: "",
        location_color: "#ffa51f",
        location_opacity: 0.8,
        location_size: 25,
        location_type: "square",
        location_image_source: "frog.png",
        location_border_color: "#FFFFFF",
        location_border: 2,
        all_locations_inactive: "no",
        all_locations_hidden: "no",

        //Label defaults
        label_color: "#ffffff",
        label_hover_color: "#ffffff",
        label_size: 16,
        label_font: "Arial",
        label_display: "auto",
        label_scale: "yes",
        hide_labels: "no",
        hide_eastern_labels: "no",

        //Zoom settings
        zoom: "no",
        manual_zoom: "no",
        back_image: "no",
        initial_back: "no",
        initial_zoom: "-1",
        initial_zoom_solo: "no",
        region_opacity: 1,
        zoom_out_incrementally: "yes",
        zoom_percentage: 0.99,
        zoom_time: 0.5,

        //Popup settings
        popup_color: "white",
        popup_opacity: 0.9,
        popup_shadow: 1,
        popup_corners: 5,
        popup_font: "12px/1.5 Verdana, Arial, Helvetica, sans-serif",
        popup_nocss: "no",

        //Advanced settings
        div: "map",
        auto_load: "yes",
        url_new_tab: "no",
        images_directory: "default",
        fade_time: 0.1,
        link_text: "View Website",
        popups: "detect",
        state_image_url: "",
        state_image_position: "",
        location_image_url: "",
    },
    state_specific: {
        PE: {
            inactive: "yes",
        },
    },
    locations: {
        0: {
            name: "Lima",
            lat: "-12.0464",
            lng: "-77.0428",
            description: "Capital of Peru",
            url: "/",
        },
        1: {
            name: "Cusco",
            lat: "-13.5317",
            lng: "-71.9675",
            description: "Gateway to Machu Picchu",
            url: "/",
        },
        2: {
            name: "Machu Picchu",
            lat: "-13.1631",
            lng: "-72.5450",
            description: "Ancient Inca citadel",
            url: "/",
        },
        3: {
            name: "Arequipa",
            lat: "-16.4090",
            lng: "-71.5375",
            description: "The White City",
            url: "/",
        },
        4: {
            name: "Iquitos",
            lat: "-3.7437",
            lng: "-73.2516",
            description: "Gateway to the Amazon",
            url: "/",
        },
        5: {
            name: "Nazca",
            lat: "-14.8322",
            lng: "-74.9381",
            description: "Home of the Nazca Lines",
            url: "/",
        },
        6: {
            name: "Huacachina",
            lat: "-14.0875",
            lng: "-75.7626",
            description: "Desert oasis near Ica",
            url: "/",
        },
    },
    labels: {
        PE: {
            name: "Peru",
            parent_id: "PE",
        },
    },
    legend: {
        entries: [],
    },
    regions: {},
};
