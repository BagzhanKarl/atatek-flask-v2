FamilyTree.templates.ataTek = Object.assign({}, FamilyTree.templates.tommy);
FamilyTree.templates.ataTek.size = [230, 80];

FamilyTree.templates.ataTek.defs = ``;


FamilyTree.templates.ataTek.name =
    `<text style="font-size: 16px;" fill="#ffffff" x="20" y="60" text-anchor="start">{val}</text>`;

FamilyTree.templates.ataTek.birthday =
    `<text style="font-size: 12px;" fill="#ffffff" x="20" y="80" text-anchor="start">{val}</text>`;

FamilyTree.templates.ataTek.death =
    `<text style="font-size: 12px;" fill="#ffffff" x="85" y="80" text-anchor="start">{val}</text>`;


FamilyTree.templates.ataTek.link =
    `<path stroke="#686868" stroke-width="1px" fill="none" data-l-id="[{id}][{child-id}]" 
    d="M{xa},{ya} L{xb},{yb} L{xc},{yc} L{xd},{yd}" />`;


FamilyTree.templates.ataTek.nodeMenuButton =
    `<g style="cursor:pointer;" transform="matrix(1,0,0,1,205,18)" data-ctrl-n-menu-id="{id}">
        <rect x="-4" y="-10" fill="#000000" fill-opacity="0" width="22" height="22"></rect>
        <circle cx="2.5" cy="0" r="1.5" fill="rgb(255, 255, 255)" />
        <circle cx="2.5" cy="5" r="1.5" fill="rgb(255, 255, 255)" />
        <circle cx="2.5" cy="10" r="1.5" fill="rgb(255, 255, 255)" />
    </g>`;


FamilyTree.templates.ataTek_male = Object.assign({}, FamilyTree.templates.ataTek);
FamilyTree.templates.ataTek_male.node = `
    <rect rx="10" ry="10" x="10" y="10" width="210" height="80" 
    fill="#A8D07A" stroke="#686868" stroke-width="2"></rect>
`;
FamilyTree.templates.ataTek_female = Object.assign({}, FamilyTree.templates.ataTek);
FamilyTree.templates.ataTek_female.node = `
    <rect rx="10" ry="10" x="10" y="10" width="210" height="80" 
    fill="#FFB6C1" stroke="#686868" stroke-width="2"></rect>
`;


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

async function initFamilyTree() {
    const myFamily = await loadFamilyData(); // Ждем загрузки данных



    var family = new FamilyTree(document.getElementById("tree"), {
        mouseScrool: FamilyTree.action.none,
        template: "ataTek",
        enableSearch: false,
        nodeTreeMenu: true,
        nodeBinding: {
            name: "name",
            birthday: "birthday",
            death: "death",
        },
        nodeMenu: {
            edit: { text: "Өзгерту" }
        },
        editForm: {
            generateElementsFromFields: false,
            elements: [
                { type: 'textbox', label: 'Толық есімі', binding: 'name' },
                { type: 'textbox', label: 'Туған күні', binding: 'birthday' },
            ],
            cancelBtn: 'Жабу',
            saveAndCloseBtn: 'Сақтау',
            addMore: false,
            buttons:  {
                edit: {
                    icon: FamilyTree.icon.edit(24,24,'#fff'),
                    text: 'Өзгерту',
                    hideIfEditMode: true,
                    hideIfDetailsMode: false
                },
                share: {
                    icon: FamilyTree.icon.share(24,24,'#fff'),
                    text: 'Бөлісу'
                },
                pdf: null
            },
            titlePhoto: false,
        },
    });

    family.on('update', function (sender, oldNode, newNode) {
        console.log(oldNode);
    });


    family.load(myFamily);

}

// Инициализация дерева при загрузке страницы
window.addEventListener("load", initFamilyTree);