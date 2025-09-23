function tool(msg, duration){
    console.log(msg)
    const tool_el = document.createElement("div");
    tool_el.id = "tool";

    const tool_item = document.createElement("div");
    tool_item.id = "tool-item";
    tool_item.textContent = msg;

    tool_el.append(tool_item);
    
    document.body.append(tool_el);

    setTimeout(() => {tool_el.remove()}, duration);
}

async function get_endpoint(endpoint, opts) {
    console.log(endpoint, opts)
    const req = await fetch(endpoint, opts);

    if(!req.ok){
        json = await req.json();

        tool(json?.msg, 3000);
    }

    return await req.json();
};

async function get_path(path){
    const paths = await get_endpoint("/get-path", 
        {
            method:"POST",
            headers:{
                "Content-Type":"application/json"
            },
            body:JSON.stringify({path:path})
        }
    )

    if(!paths){
        return;
    }

    load_paths(paths);
}

async function add_path(){
    
}
tool("Test", 5000);