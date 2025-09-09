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
        MX: {
            inactive: "yes",
        },
    },
    locations: {
        0: {
            name: "Mexico City",
            lat: "19.4326",
            lng: "-99.1332",
            description: "Capital of Mexico",
            url: "/",
            image_url: "/static/images/map_pins/pin1.svg",
        },
        1: {
            name: "Cancún",
            lat: "21.1619",
            lng: "-86.8515",
            description: "Famous Caribbean beach resort",
            url: "/",
            image_url: "/static/images/map_pins/pin2.svg",
        },
        2: {
            name: "Chichen Itza",
            lat: "20.6843",
            lng: "-88.5678",
            description: "Ancient Mayan city",
            url: "/",
            image_url: "/static/images/map_pins/pin3.svg",
        },
        3: {
            name: "Guadalajara",
            lat: "20.6597",
            lng: "-103.3496",
            description: "Birthplace of mariachi music",
            url: "/",
            image_url: "/static/images/map_pins/pin4.svg",
        },
        4: {
            name: "Tulum",
            lat: "20.2114",
            lng: "-87.4654",
            description: "Coastal Mayan ruins",
            url: "/",
            image_url: "/static/images/map_pins/pin5.svg",
        },
        5: {
            name: "Puerto Vallarta",
            lat: "20.6534",
            lng: "-105.2253",
            description: "Pacific coast resort city",
            url: "/",
            image_url: "/static/images/map_pins/pin6.svg",
        },
        6: {
            name: "Oaxaca",
            lat: "17.0732",
            lng: "-96.7266",
            description: "Cultural and culinary capital",
            url: "/",
            image_url: "/static/images/map_pins/pin7.svg",
        },
    },
    labels: {
        MX: {
            name: "Mexico",
            parent_id: "MX",
        },
    },
    legend: {
        entries: [],
    },
    regions: {},
};
