(() => {
    const path_list = document.createElement("div");
    path_list.id = "path_list";
    document.body.appendChild(path_list);


    function tool(msg, duration) {
        console.log(msg)
        const tool_el = document.createElement("div");
        tool_el.id = "tool";

        const tool_item = document.createElement("div");
        tool_item.id = "tool-item";
        tool_item.textContent = msg;

        tool_el.append(tool_item);

        document.body.append(tool_el);

        setTimeout(() => { tool_el.remove() }, duration);
    }

    async function get_endpoint(endpoint, opts) {
        console.log(endpoint, opts)
        const req = await fetch(endpoint, opts);

        if (!req.ok) {
            json = await req.json();

            tool(json?.msg, 3000);
        }

        return await req.json();
    };

    async function get_path(path) {
        const paths = await get_endpoint("/get-path",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ path: path })
            }
        )

        if (!paths) {
            return;
        }

        load_paths(paths);
    }

    async function add_path() {

    }

    async function change_path(path) {

    }


    function load_paths(paths) {

        for (path in paths) {

        }
    }

    function handle_path(path, type) {
        const element = document.createElement("div");
        element.className = "path";

        const icon_d = document.createElement("div");
        icon_d.className = "path-icon-d";
        element.append(icon_d);

        const icon = document.createElement("img");
        icon.className = "path-icon";
        icon.src = `/icon/${type}`;
        icon_d.append(icon);

        const name_d = document.createElement("div");
        name_d.className = "path-name-d";
        element.append(name_d);

        const name = document.createElement("span");
        name.className = "path-name";
        name.textContent = path;
        name.ondblclick = () => {
            name.contentEditable = true;
        }
        name.onchange = () => {
            change_path(path, name.textContent);   
        }
        name_d.append(name);


    }

})();