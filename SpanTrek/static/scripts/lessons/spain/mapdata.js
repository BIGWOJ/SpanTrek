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
        ES: {
            inactive: "yes",
        },
    },
    locations: {
        0: {
            name: "Madrid",
            lat: "40.4178",
            lng: "-3.6947",
            description: "Capital of Spain",
            url: "/",
            image_url: "/static/images/map_pins/pin1.svg",
        },
        1: {
            name: "Barcelona",
            lat: "41.3851",
            lng: "2.1734",
            description: "Capital of Catalonia",
            url: "/",
            image_url: "/static/images/map_pins/pin2.svg",
        },
        2: {
            name: "Valencia",
            lat: "39.4699",
            lng: "-0.3763",
            description: "Home of paella",
            url: "/",
            image_url: "/static/images/map_pins/pin3.svg",
        },
        3: {
            name: "Seville",
            lat: "37.3891",
            lng: "-5.9845",
            description: "Capital of Andalusia",
            url: "/",
            image_url: "/static/images/map_pins/pin4.svg",
        },
        4: {
            name: "Bilbao",
            lat: "43.2630",
            lng: "-2.9350",
            description: "Basque Country's largest city",
            url: "/",
            image_url: "/static/images/map_pins/pin5.svg",
        },
        5: {
            name: "Málaga",
            lat: "36.7213",
            lng: "-4.4217",
            description: "Picasso's birthplace",
            url: "/",
            image_url: "/static/images/map_pins/pin6.svg",
        },
        6: {
            name: "Ibiza",
            lat: "38.9067",
            lng: "1.4206",
            description: "Famous party island in the Balearics",
            url: "/",
            image_url: "/static/images/map_pins/pin7.svg",
        },
        7: {
            name: "Palma de Mallorca",
            lat: "39.5696",
            lng: "2.6502",
            description: "Capital of the Balearic Islands",
            url: "/",
            image_url: "/static/images/map_pins/pin8.svg",
        },
        8: {
            name: "Santa Cruz de Tenerife",
            lat: "28.4683",
            lng: "-16.2546",
            description: "Capital of the Canary Islands",
            url: "/",
            image_url: "/static/images/map_pins/pin9.svg",
        },
    },
    labels: {
        ES: {
            name: "Spain",
            parent_id: "ES",
        },
    },
    legend: {
        entries: [],
    },
    regions: {},
};
