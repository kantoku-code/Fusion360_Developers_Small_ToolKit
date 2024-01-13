// fusion360 api

const DEBUG = true

document.addEventListener("DOMContentLoaded", () => {
    let adskWaiter = setInterval(() => {
        dumpLog("DOMContentLoaded");
        if (window.adsk) {
            dumpLog("adsk ok");
            clearInterval(adskWaiter);

            adsk
            .fusionSendData("DOMContentLoaded", "{}")
            .then((data) => {
                dumpLog(data)
                const button_info = JSON.parse(data)
                initMenu(button_info)
            });
        }
    }, 100);
});

window.fusionJavaScriptHandler = {
    handle: function (action, data) {
        try {
            if (action === "command_event") {
                let values = JSON.parse(data);
                dumpLog(values['value']);
                setDisabledByButton(toBoolean(values["value"]), "button");
            } else if (action === "debugger") {
                debugger;
            } else {
                return `Unexpected command type: ${action}`;
            }
        } catch (e) {
            console.log(e);
            console.log(`Exception caught with command: ${action}, data: ${data}`);
        }
        return "OK";
    },
};

function initMenu(button_info) {

    const button_group = document.getElementById("Instant_Menu")

    const divContainer = document.createElement("div");
    divContainer.setAttribute("class", "container");
    button_group.appendChild(divContainer)

    const divRow = document.createElement("div");
    divRow.setAttribute("class", "row g-1");
    divContainer.appendChild(divRow);

    for (const info in button_info) {

        const category = button_info[info]

        const divCategory = document.createElement("div");
        divCategory.setAttribute("class", "col-12");
        divRow.appendChild(divCategory);

        const divBorder = document.createElement("div");
        divBorder.setAttribute("class", "p-1 border bg-light");
        divCategory.appendChild(divBorder);


        for (const btnInfo of category["buttons"]) {
            switch (btnInfo["btn_type"]) {
            case "switch":
                divBorder.appendChild(initSwitch(btnInfo));
                let switch_input = document.getElementById(btnInfo['id']);
                switch_input.addEventListener('change',function(){
                    let args = {
                        id: btnInfo['id'],
                        value: switch_input.checked
                    };
                    adsk.fusionSendData("switch_event", JSON.stringify(args));
                });
                break;
            case "switch_check":
                divBorder.appendChild(initSwitch_Check(btnInfo));

                let sw_input = document.getElementById(btnInfo['id']);
                let ch_input= document.getElementById(btnInfo['id'] + "_check");
                sw_input.addEventListener('change',function(){
                    setDisabledById(!sw_input.checked, btnInfo['id'] + "_check")

                    let args = {
                        id: btnInfo['id'],
                        sw_value: sw_input.checked,
                        ch_value: ch_input.checked,
                    };
                    adsk.fusionSendData("switch_check_event", JSON.stringify(args));
                });
                ch_input.addEventListener('change',function(){
                    let args = {
                        id: btnInfo['id'],
                        sw_value: sw_input.checked,
                        ch_value: ch_input.checked,
                    };
                    adsk.fusionSendData("switch_check_event", JSON.stringify(args));
                });
                break;
            default:
                divBorder.appendChild(init_Button(btnInfo));
                break;
            }
        }
    }
}

function initSwitch_Check(button_info) {
    // switch
    const switch_check_div = document.createElement("div");

    const switch_div = initSwitch(button_info);
    switch_check_div.appendChild(switch_div);

    const check_div = initCheck(button_info);
    switch_check_div.appendChild(check_div);

    return switch_check_div
}


function initSwitch(button_info) {
    // div
    const switch_div = document.createElement("div");
    switch_div.setAttribute("class", "form-check form-switch form-check-inline");
    switch_div.setAttribute("data-bs-toggle", "tooltip");
    switch_div.setAttribute("data-bs-placement", "top");
    switch_div.setAttribute("title", button_info["tooltip"]);

    // input
    const switch_input = document.createElement("input");
    switch_input.setAttribute("class", "form-check-input");
    switch_input.type = "checkbox";
    switch_input.id = button_info['id'];
    switch_div.appendChild(switch_input);

    // label
    const switch_label = document.createElement("label");
    switch_label.setAttribute("class", "form-check-label");
    switch_label.for = button_info['id'];
    switch_label.textContent = button_info['name']
    switch_div.appendChild(switch_label);

    return switch_div
}


function initCheck(button_info) {
    // div
    const check_div = document.createElement("div");
    check_div.setAttribute("class", "form-check form-check-inline");
    check_div.setAttribute("data-bs-toggle", "tooltip");
    check_div.setAttribute("data-bs-placement", "top");
    check_div.setAttribute("title", button_info["check_tooltip"]);

    // checkbox
    const check_children = document.createElement("input");
    check_children.setAttribute("class", "form-check-input");
    check_children.setAttribute("id", button_info['id'] + "_check");
    check_children.setAttribute("type", "checkbox");
    check_children.setAttribute("value", "");
    check_children.setAttribute("disabled", "true");
    check_div.appendChild(check_children);

    // label
    const label_children = document.createElement("label");
    label_children.setAttribute("class", "form-check-label");
    label_children.setAttribute("for", button_info['id'] + "_check");
    label_children.appendChild(document.createTextNode(button_info["check_name"]));
    check_div.appendChild(label_children);

    return check_div
}


function init_Button(button_info) {
    const btn = document.createElement("button");
    btn.setAttribute("class", "btn btn-outline-secondary btn-sm customBtn");
    btn.setAttribute("id", button_info['id']);
    btn.setAttribute("data-bs-toggle", "tooltip");
    btn.setAttribute("data-bs-placement", "top");
    btn.setAttribute("title", button_info["tooltip"]);
    btn.innerHTML = button_info['icon'];
    btn.addEventListener('click',function(){
        let args = {
            id: button_info['id']
        };
        adsk.fusionSendData("button_event", JSON.stringify(args));
    });
    return btn
}

function setDisabledById(value, id) {
    let elem = document.getElementById(id);
    elem.disabled = value
}

// function toBoolean(data) {
//     return data.toLowerCase() === 'true';
// }

function dumpLog(msg) {
    if (DEBUG) {
        console.log(msg);
    }
}