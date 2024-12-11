
async function loadFamilyData() {
    try {
        const response = await fetch("/my/family/get/my");
        if (!response.ok) {
            throw new Error("Failed to fetch family data");
        }

        const data = await response.json();

        const myFamily = data.map(member => {
            const formattedMember = {
                id: member.id,
                name: member.name,
                gender: member.gender,
                alive: member.alive,
                birthday: member.birthday,
            };

            if (member.mid) formattedMember.mid = member.mid;
            if (member.fid) formattedMember.fid = member.fid;
            if (member.pids) formattedMember.pids = member.pids;
            if (member.death) formattedMember.death = member.death;

            return formattedMember;
        });

        return myFamily;
    } catch (error) {
        console.error("Error loading family data:", error);
        return [];
    }
}

async function updateNotes(add, update, remove) {
    const response = await fetch("/my/family/update/my", {
        method: "POST", // Указываем метод POST
        headers: {
            "Content-Type": "application/json", // Тип данных JSON
        },
        body: JSON.stringify({ add, update, remove }), // Преобразуем объект в JSON-строку
    });

    if (!response.ok) {
        throw new Error(`Ошибка: ${response.status}`);
    }
    console.log(response);
    window.location.reload();
    return await response.json(); // Предполагаем, что сервер возвращает JSON
}


async function initFamilyTree() {
    const myFamily = await loadFamilyData(); // Ждем загрузки данных

    var family = new FamilyTree(document.getElementById("tree"), {
        mouseScrool: FamilyTree.action.scroll,
        template: "ataTek",
        enableSearch: false,
        nodeBinding: {
            name: "name",
            birthday: "birthday",
            death: "death",
        },
        editForm: {
            readOnly: true,
            generateElementsFromFields: false,
            elements: [
                { type: 'textbox', label: 'Толық есімі', binding: 'name' },
                { type: 'textbox', label: 'Туған күні', binding: 'birthday' },
                { type: 'select', label: 'Статус',  options: [
                    {value: true, text: 'Тірі'},
                    {value: false, text: 'Қайтыс болды'}], binding: 'alive'}
            ],
            
        },

    });

    family.on('update', function (sender, oldNode, newNode) {
        updateNotes(oldNode.addNodesData, oldNode.updateNodesData, oldNode.removeNodeId);
    });


    family.load(myFamily);
    console.log(myFamily)

}

// Инициализация дерева при загрузке страницы
window.addEventListener("load", initFamilyTree);