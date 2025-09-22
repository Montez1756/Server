function tool(msg, duration){
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
    const req = await fetch(endpoint, opts);


}

tool("Test", 5000);