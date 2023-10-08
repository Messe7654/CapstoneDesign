const toolList = document.querySelector('#tool');
const optionList = document.querySelector('.option')

function selectTool(){
    let preSelect = document.querySelector('.selected');
    
    preSelect.classList.remove('selected');
    this.classList.add('selected');

}
for(let i=0; i<toolList.childElementCount; i++)
{
    toolList.children[i].addEventListener('click', selectTool);

}


