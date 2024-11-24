const nameProperty = 'name';
const link = '/api/tree/get/childs';
const STROKE_WIDTH = theme.sizes.stroke;
const CORNER_ROUNDNESS = theme.sizes.radius;

function strokeStyle(shape) {
    return shape
        .set({
            fill: theme.colors.personNodeBackground,
            strokeWidth: STROKE_WIDTH
        })
        .bind('fill', theme.colors.personNodeBackground);
}

const personBadge = () => {
    const badge = new go.Panel('Auto', {
        alignmentFocus: go.Spot.TopRight,
        alignment: new go.Spot(1, 0, -10, STROKE_WIDTH - 0.5),
        visible: false
    }).add(
        new go.Shape({
            figure: 'RoundedRectangle',
            parameter1: CORNER_ROUNDNESS,
            desiredSize: new go.Size(NaN, 13),
            stroke: null,
            fill: theme.colors.BadgeBackground
        }),
        new go.TextBlock({
            font: theme.fonts.badgeFont,
            stroke: theme.colors.BadgeText,
            text: "Ақпарат"
        })
    );

    badge.click = (e, obj) => {
        openInfo(obj.part.data.id);
        e.handled = true;
    };

    return badge;
};


const personBirthDeathTextBlock = () => new go.TextBlock(
    {
        stroke: theme.colors.personText,
        font: theme.fonts.birthDeathFont,
        alignmentFocus: go.Spot.Top,
        alignment: new go.Spot(0.5, theme.sizes.dateTop, 0, -35)
    }).bind('text', '', ({born, death}) => {
    if (!born) return ''; return `${born} - ${death ?? ''}`;
})

const personMainShape = () => new go.Shape({
    figure: 'RoundedRectangle',
    desiredSize: new go.Size(theme.sizes.nodeX, theme.sizes.nodeY),
    portId: '',
    parameter1: Math.min(theme.sizes.nodeX, theme.sizes.nodeY) / 2  // Округление углов на 50% от размеров
}).apply(strokeStyle);

const personNameTextBlock = () => new go.TextBlock({
    stroke: theme.colors.personText,
    font: theme.fonts.nameFont,
    desiredSize: new go.Size(theme.sizes.textX, theme.sizes.textY),
    overflow: go.TextOverflow.Ellipsis,
    textAlign: 'center',
    verticalAlignment: go.Spot.Center,
    alignmentFocus: go.Spot.Top,
    alignment: new go.Spot(0.5, theme.sizes.textTop, 0, 25)
}).bind('text', nameProperty)

const createNodeTemplate = () => new go.Node('Spot',
    {
        selectionAdorned: false,
        movable: false,
        click: async (e, node) => {
            console.log('Клик');
            if(node.data.untouchable == false) {
                if (node.isTreeExpanded && node.findTreeChildrenNodes().count > 0) {
                    diagram.commandHandler.collapseTree(node);
                } else {
                    if (node.data.isLoaded) {
                        diagram.commandHandler.expandTree(node);
                        console.log('Данные уже загружены, просто разворачиваем узел');
                    } else {
                        try {
                            console.log('Запрос данных...');
                            const result = await fetchAndAddFamilyData(node.data.id, node.data.name);
                            if (result.length > 0) {
                                diagram.model.addNodeDataCollection(result);
                                diagram.updateAllTargetBindings();

                                diagram.model.setDataProperty(node.data, "isLoaded", true);

                                diagram.commandHandler.expandTree(node);
                                console.log('Данные загружены и узел развернут');

                                const clickedNode = diagram.findNodeForKey(node.data.id);
                                if (clickedNode) {
                                    diagram.centerRect(clickedNode.actualBounds);
                                }
                            }
                        } catch (error) {
                            console.error('Ошибка при загрузке данных:', error);
                        }
                    }
                }


                if (!e.handled) {
                    e.handled = true;
                }
            }
        },
        contextClick: (e, node) => {
            if(node.data.role != 1){
                console.log(`Имя: ${node.data.name}, ID: ${node.data.id}`);
                e.handled = true;
                openInfo(node.data.id);
            }

        }
    }).add(
    new go.Panel('Spot').add(
        personMainShape(),
        personNameTextBlock(),
        personBirthDeathTextBlock()
    ),
    personBadge().bind('visible', 'info', (info) => info === true)
);


const createLinkTemplate = () => new go.Link({
    routing: go.Link.Normal,  // Линии будут естественными, с лёгким изгибом, как на примере
    curve: go.Link.Bezier,  // Используем кривизну Бейзье для мягких плавных линий
    curviness: 100,  // Устанавливаем небольшое значение, чтобы добиться нужного изгиба, как на примере
    layerName: 'Background',  // Линии находятся на заднем плане
    selectionAdorned: false,  // Отключаем выделение линий при выборе узлов
}).add(new go.Shape({
    stroke: theme.colors.link,  // Цвет линии из темы
    strokeWidth: 2  // Толщина линии, можно настроить для получения нужного эффекта
}));

let diagram;
const initDiagram = (divId) => {
    diagram = new go.Diagram(divId, {
        layout: new go.TreeLayout({
            angle: 90,  // Горизонтальная раскладка для более удобного отображения дочерних узлов
            nodeSpacing: theme.sizes.nodespace,  // Расстояние между узлами на одном уровне
            layerSpacing: theme.sizes.layerspace,  // Расстояние между уровнями для лучшего визуального отделения
            treeStyle: go.TreeStyle.Layered,  // Стиль, который группирует узлы более симметрично
            alternateAngle: 0,
            alternateAlignment: go.TreeAlignment.Start,  // Начальное выравнивание для дочерних элементов
            alternateNodeSpacing: 30,
        }),

        'toolManager.hoverDelay': 100,
        linkTemplate: createLinkTemplate(),
        model: new go.TreeModel({
            nodeKeyProperty: 'id'
        })
    });

    diagram.toolManager.contextMenuTool.isEnabled = false;
    // Добавляем нужные параметры для улучшения поведения диаграммы
    diagram.initialAutoScale = go.Diagram.Uniform;  // Автоматическое масштабирование диаграммы
    diagram.isViewportSized = false;  // Разрешаем диаграмме быть больше видимой области
    diagram.scrollMode = go.Diagram.InfiniteScroll;  // Отключаем ограничения на область прокрутки

    diagram.animationManager.isEnabled = true;  // Включаем анимацию
    diagram.animationManager.duration = 1000;  // Длительность анимации (в миллисекундах)

    diagram.nodeTemplate = createNodeTemplate();
    diagram.model.nodeDataArray = familyData;

    const root = diagram.findNodeForKey(14);
    diagram.scale = 0.75;
};


window.addEventListener('DOMContentLoaded', () => {
    initDiagram('myDiagramDiv');
    setTimeout(() => {

    }, 300);
});

let currentAngle = 90; // начальное значение угла

function toggleAngle() {
    $('.a' + currentAngle).hide();
    // Переключаем угол между 0 и 90
    currentAngle = currentAngle === 90 ? 0 : 90;

    $('.a' + currentAngle).show();

    // Применяем новый угол к текущей раскладке
    diagram.layout.angle = currentAngle;

    // Обновляем диаграмму для применения изменений
    diagram.layoutDiagram(true);
}

async function fetchAndAddFamilyData(id, name) {
    try {
        showLoader();
        const response = await fetch(link, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ parent_id: id }),
        });

        const result = await response.json();

        if (result.status) {
            hideLoader();
            const newMembers = result.data
                .map(member => ({
                    id: parseInt(member.id),
                    name: member.name,
                    born: member.birth,
                    death: member.death,
                    parent: parseInt(member.parent_id),
                    info: member.info,
                    untouchable: member.untouchable,
                    role: member.role
                }));

            if (newMembers.length === 0) {
                noDate(name);
                return [];
            }

            const existingIds = new Set(familyData.map(member => member.id));
            const filteredNewMembers = newMembers.filter(member => !existingIds.has(member.id));

            if (filteredNewMembers.length > 0) {
                familyData.push(...filteredNewMembers);
                return filteredNewMembers;
            }
        } else {
            hideLoader();
            console.error('Error in API response');
        }
    } catch (error) {
        hideLoader();
        console.error('Fetch error:', error);
    }
    return [];
}


document.getElementById('toggleAngle').addEventListener('click', toggleAngle);
document.addEventListener('contextmenu', (e) => e.preventDefault());