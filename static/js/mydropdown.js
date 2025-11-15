// Get elements
const dpLabel = document.getElementById("Preference");
// const mainDropdown = document.querySelector('.dropdown-content.main');
const mainDropdown = document.getElementById('list-container');
const submenus = document.querySelectorAll('.submenu');

const dropdown = document.querySelector('.dropdown');
const toggleBtn = dropdown.querySelector('.dropdown-toggle'); // The “Mouse over me!” text

// Track currently open submenu
let activeSubmenu = null;

// Toggle main dropdown when clicking the label
toggleBtn.addEventListener('click', (e) => {
  e.stopPropagation(); // Prevent closing immediately
  const isVisible = mainDropdown.style.display === 'block';

  // Close active submenu if any
  if (activeSubmenu) {
    activeSubmenu.style.display = 'none';
    activeSubmenu.classList.remove('active');
    activeSubmenu = null;
  }

  // Toggle main dropdown
  mainDropdown.style.display = isVisible ? '' : 'block';
});

//====================================================
// PURPOSE: saves new added prefernce
//====================================================
//HANDEL the form submit 
const addButton = document.getElementById("add-preference-button");
addButton.addEventListener('click', (e) => {
    e.stopPropagation();
    mainDropdown.style.display = 'none';

    // Close currently open submenu if another is open
    if (activeSubmenu) {
    activeSubmenu.style.display = 'none';
    activeSubmenu.classList.remove('active');
    }

    const addSubmenu = document.getElementById(`submenu-add`);
    if (addSubmenu) {
    addSubmenu.style.display = 'block';
    addSubmenu.classList.add('active');
    activeSubmenu = addSubmenu;
    }

    //add event to add menu back btn.
    const addbackBtn = addSubmenu.querySelector(".back-btn");
    addbackBtn.addEventListener('click', (e)=>{
      editBackButton();
    });
    //add event to add menu save/submit btn.
    const addSaveBtn = addSubmenu.querySelector(".submit-btn");
    const addForm = addSubmenu.querySelector(".add-form");
    addSaveBtn.addEventListener('click', (e)=>{
      const id = Object.keys(menuData).length + 1;
      const label = addForm.elements["pname"].value;
      console.log(id, label);
      saveEditBtn(e, addForm, id, label);
      // editBackButton();
    });
});
//=======================================
// **************** END *****************
//=======================================

// Close everything when clicking outside
document.addEventListener('click', (e) => {
  if (!dropdown.contains(e.target)) {
    // Hide main dropdown
    mainDropdown.style.display = '';

    // Hide active submenu (if any)
    if (activeSubmenu) {
      activeSubmenu.style.display = 'none';
      activeSubmenu.classList.remove('active');
      activeSubmenu = null;
    }
  }
});

// let menuData = JSON.parse(localStorage.getItem("menuData")) || [];
// let menuData = {
//   1:{
//     "id": 1,
//     "name": "Fruits",
//     "children": [
//       { "id": 11, "ccmin": 0 },
//       { "id": 12, "ccmax": 100 },
//       { "id": 13, "wcmin": 0 },
//       { "id": 14, "wcmax": null },
//       { "id": 15, "scmin": 0 },
//       { "id": 16, "scmax": null },
//       { "id": 17, "stcmin": 0 },
//       { "id": 18, "stcmax": null },
//       { "id": 19, "pcmin": 0 },
//       { "id": 110, "pcmax": null },
//       { "id": 111, "rtmin": 0 },
//       { "id": 112, "rtmax": null}
//     ]
//   },
//   2:{
//     "id": 2,
//     "name": "Vegetables",
//     "children": [
//       { "id": 11, "ccmin": 0 },
//       { "id": 12, "ccmax": null },
//       { "id": 13, "wcmin": 0 },
//       { "id": 14, "wcmax": null },
//       { "id": 15, "scmin": 0 },
//       { "id": 16, "scmax": null },
//       { "id": 17, "stcmin": 0 },
//       { "id": 18, "stcmax": null },
//       { "id": 19, "pcmin": 0 },
//       { "id": 110, "pcmax": null },
//       { "id": 111, "rtmin": 0 },
//       { "id": 112, "rtmax": null}
//     ]
//   }
// };

//load data from localStorage
let menuData = JSON.parse(localStorage.getItem("menuData")) || {};

//====================================================
// PURPOSE: saves edited preference
//====================================================
function saveEditBtn(event, editForm, id, label){
    event.preventDefault();
    //get the edit form fields
    const ccmin = editForm.elements["ccmin"].value;
    const ccmax = editForm.elements["ccmax"].value;

    const wcmin = editForm.elements["wcmin"].value;
    const wcmax = editForm.elements["wcmax"].value;

    const scmin = editForm.elements["scmin"].value;
    const scmax = editForm.elements["scmax"].value;

    const stcmin = editForm.elements["stcmin"].value;
    const stcmax = editForm.elements["stcmax"].value;

    const pcmin = editForm.elements["pcmin"].value;
    const pcmax = editForm.elements["pcmax"].value;

    const rtmin = editForm.elements["rtmin"].value;
    const rtmax = editForm.elements["rtmax"].value;


    const data = [
      { "id": 11, "ccmin": ccmin },
      { "id": 12, "ccmax": ccmax },
      { "id": 13, "wcmin": wcmin },
      { "id": 14, "wcmax": wcmax },
      { "id": 15, "scmin": scmin },
      { "id": 16, "scmax": scmax },
      { "id": 17, "stcmin": stcmin },
      { "id": 18, "stcmax": stcmax },
      { "id": 19, "pcmin": pcmin },
      { "id": 110, "pcmax": pcmax },
      { "id": 111, "rtmin": rtmin },
      { "id": 112, "rtmax":rtmax }
    ]

    //to be used to add new data
    // Check or create nested structure
  if (!menuData[`${id}`]) menuData[`${id}`] = {};
  if (!menuData[`${id}`].id) menuData[`${id}`].id = id;
  if (!menuData[`${id}`].name) menuData[`${id}`].name = label;
  if (!menuData[`${id}`].children) menuData[`${id}`].children = data;
  else { //editting the data
    menuData[`${id}`].children = data; // saveEditBtn(id, label, data);
    }
    //save the data back into localStorage.
    localStorage.setItem("menuData", JSON.stringify(menuData));
    //refresh the menu
    renderMenu(menuData);
    alert(`Preference "${label}" saved.`);
}

//====================================================
// PURPOSE: only closes the currently opened edit menu
//====================================================
function editBackButton(){
     if (activeSubmenu) {
      activeSubmenu.style.display = 'none';
      activeSubmenu.classList.remove('active');
      activeSubmenu = null;
    }

    mainDropdown.style.display = 'block';
}
//===============================================
// PURPOSE: only opens the currently selected preference's edit menu
//===============================================
function editListItem(id, label){
  console.log("getting into editList");
  mainDropdown.style.display = 'none';

  // Close currently open submenu if another is open
      if (activeSubmenu) {
        activeSubmenu.style.display = 'none';
        activeSubmenu.classList.remove('active');
      }

      const submenu = document.getElementById(`submenu-${id}`);
      if (submenu) {
        submenu.style.display = 'block';
        submenu.classList.add('active');
        activeSubmenu = submenu;
      }
}

//===============================================
// PURPOSE: deletes a preference item
//===============================================
function delPreferenceBtn(id, label){
  if (!confirm(`You want to delete preference ${label}?`)) return;
  delete menuData[id];
  //save back into localStorage
  localStorage.setItem("menuData", JSON.stringify(menuData));
  alert(`Preference ${label} is deleted.`);
  renderMenu(menuData);
}
//========================================================
// COMPONENT: Renders the menu  dynamically
// DESCRIPTION: renderMenu() pushes each parent and its children iteratively into renderMenuItems() to render it as follows:
// Step1:
// - create the parent prf. item
// - edit the properties from the localstorage data of the prf. item
// - add event (del, edit) to its buttons.
// - append the prf. item into the dropdown.
// Step2:
// - create the child item.
// -  fill its properties from its parent's data in the localStorage.
// - add events (back, save) to its buttons.
// - append the child into the dropdown.
//=========================================================
function renderMenu(data){
  const container = document.getElementById("preference-list");
  container.innerHTML = ""; //empty the inside before putting something

  //msg to show inside preference-list when its no preferences exist.
  if (Object.keys(data).length == 0) {
    const msg = document.createElement("code");
    msg.innerText = "Add preference please.";
    container.appendChild(msg);
  }
  
  // data.forEach(item =>{
  //   renderMenuItem(item.id, item.name, item.children);
  // });
  Object.entries(data).forEach(([parentId, parentItem]) => {
    renderMenuItem(parentId, parentItem.name, parentItem.children);
  });
}
function renderMenuItem(id, label, childData){

  const container = document.getElementById("preference-list");
  const pTemplate = document.getElementById("preference-template");

  //S1: create the parent item.

  // Clone the parent item template
  const clone = pTemplate.content.cloneNode(true);

  // Select elements inside the clone
  const div = clone.querySelector("div");
  const p = clone.querySelector(".item-name");
  

  // Set dynamic values
  div.id = id;
  p.textContent = label;
  p.dataset.type = label;

  //attach events to the buttons
  const delBtn = clone.querySelector(".delete-preference");
  const editBtn = clone.querySelector(".edit-preference");

  delBtn.addEventListener('click', (e) =>{
    delPreferenceBtn(id, label);
  });

  editBtn.addEventListener('click', (e) =>{
    editListItem(id, label);
  });

  //add to DOM
  container.appendChild(clone);

  //S2: create the child item.//
  const cTemplate = document.getElementById("edit-template");
  const dropdown = document.getElementById("dropdown");
  const cClone = cTemplate.content.cloneNode(true);

  // Select props inside the clone to edit
  const cdiv = cClone.querySelector("div");
  const cp = cClone.getElementById("item-name");

  //set dynamic values
  cdiv.id = `submenu-${id}`;
  cp.textContent = `Edit ${label} `;

  //populate the form
  //get the edit form fields
  const editForm = cClone.querySelector("form#optionsForm");
  const formFields = ["ccmin", "ccmax", "wcmin", "wcmax", "scmin", "scmax", "stcmin", "stcmax", "pcmin", "pcmax", "rtmin", "rtmax"];

  formFields.forEach((item, index) =>{
    editForm.elements[item].value = childData[index][item];
  });

  //attach events to the buttons
  //back btn
  const cBackButton = cClone.querySelector(".back-btn");
  cBackButton.addEventListener('click', (e) =>{
    editBackButton(id, label);
  });

  //save/submit btn
  const cSaveBtn = cClone.querySelector(".submit-btn");
  cSaveBtn.addEventListener('click', (e) =>saveEditBtn(e, editForm, id, label));

  //add to DOM
  dropdown.appendChild(cClone);
}

//=======================
// DRIVER FUNCTION CALLS
//========================

//load data and render menu
renderMenu(menuData);