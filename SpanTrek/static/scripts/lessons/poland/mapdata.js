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
        location_size: 50,
        location_type: "image",
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
        PL: {
            inactive: "yes",
        },
    },
    locations: {
        0: {
            name: "Szczecin",
            lat: "53.4285",
            lng: "14.5528",
            description: "Major seaport city",
            url: "/lessons/poland/szczecin/",
            image_url: "/static/images/map_pins/pin1.svg",
        },
        1: {
            name: "Krakow",
            lat: "50.0647",
            lng: "19.9450",
            description: "Historical capital and cultural center",
            url: "/lessons/poland/krakow/",
            image_url: "/static/images/map_pins/pin2.svg",
        },
        2: {
            name: "Gdansk",
            lat: "54.3520",
            lng: "18.6466",
            description: "Port city on the Baltic Sea",
            url: "/lessons/poland/gdansk/",
            image_url: "/static/images/map_pins/pin3.svg",
        },
        3: {
            name: "Poznan",
            lat: "52.4064",
            lng: "16.9252",
            description: "Historical trade center",
            url: "/lessons/poland/poznan/",
            image_url: "/static/images/map_pins/pin4.svg",
        },
        4: {
            name: "Warsaw",
            lat: "52.2297",
            lng: "21.0122",
            description: "Capital of Poland",
            url: "/lessons/poland/warsaw/",
            image_url: "/static/images/map_pins/pin5.svg",
        },
    },
    labels: {
        PL: {
            name: "Poland",
            parent_id: "PL",
        },
    },
    legend: {
        entries: [],
    },
    regions: {},
};
