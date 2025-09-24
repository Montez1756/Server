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



    function load_paths(paths) {

        for (path of paths) {
            handle_path(path["name"], path["type"]);
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
            name.focus();

            //Functions to stop dissallowed keys in file names
            const disallowed = ['\\', '<', '>', ':', '"', '/', '|', '*', '\''];

            // Function to handle click outside
            const handleClickOutside = (e) => {
                if (e == null || !name.contains(e.target)) { // if click is NOT inside the element
                    name.contentEditable = false;
                    document.removeEventListener("click", handleClickOutside); // remove listener
                }
            };
            document.addEventListener("click", handleClickOutside);
            name.addEventListener("keydown", (e) => {
                const key = e.key.toLowerCase();
                console.log(key)
                if (disallowed.includes(key)) {
                    e.preventDefault();
                    tool(`A file name can't contain any of the following characters: "${disallowed.join(", ")}`, 1000)
                }
                else if(key == "enter"){
                    e.preventDefault();
                    handleClickOutside(null);
                }

            });
            name.addEventListener("paste", (e) => {
                const paste = (e.clipboardData || window.clipboardData).getData('text');
                for (const char of disallowed) {
                    if (paste.includes(char)) {
                        e.preventDefault();
                        break;
                    }
                }
            })
        };
        name_d.append(name);

        path_list.append(element);
    }


    load_paths([
        { "name": "hello", "type": "file" }, { "name": "hello-dir", "type": "directory" }
    ])
})();