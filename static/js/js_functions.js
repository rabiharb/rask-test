function getDateTime() {
  let today = new Date();
  let date =
    today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
  let time = today.getHours() + ":" + today.getMinutes();
  let min_date_time =
    document.getElementsByClassName("alert-time-picker")[0].min;
  console.log(min_date_time);
  return date + "T" + time;
}
function catchDate(index) {
  let my_date_time = document.getElementsByClassName("datePicker")[index - 1];
  let task_id = document
    .getElementsByClassName("task-text")
    [index - 1].getAttribute("task_id");
  let my_due_date = document.getElementsByClassName("dueDate")[index - 1];
  // console.log(typeof my_due_date.value);
  if (my_date_time.value.trim() != "") {
    my_due_date.innerText = my_date_time.value.split("T")[0];
  } else {
    my_due_date.innerText = "Add Due Date";
  }
  my_date_time.style.display = "none";
  setDueDate(my_date_time.value.split("T")[0], task_id);
}
function toggleDate(index) {
  let datePickerList = document.getElementsByClassName("datePicker");
  for (var i = 0; i < datePickerList.length; i++) {
    if (i != index - 1) {
      datePickerList[i].style.display = "none";
    }
  }
  let my_date_time = document.getElementsByClassName("datePicker")[index - 1];
  let my_due_date = document.getElementsByClassName("dueDate")[index - 1];
  if (my_date_time.style.display == "none") {
    my_date_time.style.display = "inline-block";
    my_date_time.focus();
  } else {
    my_date_time.style.display = "none";
  }
}
let my_input = document.getElementById("userTask");
function catchValue() {
  localStorage.newTask = my_input.value;
}
function saveValue(e) {
  let keynum;

  if (window.event) {
    keynum = e.keyCode;
  } else if (e.which) {
    keynum = e.which;
  }
  if (keynum == 13) {
    my_input.blur();
  }
}
let listNameHeader = document.getElementById("editable-list-name");
function showInput() {
  let newName = listNameHeader.innerText;
  localStorage.userEdits = newName;
}
function editContent() {
  listNameHeader.setAttribute("contenteditable", "true");
}
function stopEdit(e) {
  let keynum;

  if (window.event) {
    keynum = e.keyCode;
  } else if (e.which) {
    keynum = e.which;
  }
  if (keynum == 13) {
    if (listNameHeader.innerText.trim() == "") {
      listNameHeader.innerText = "--";
    }
    listNameHeader.setAttribute("contenteditable", "false");
  }
}
function checkEdits() {
  if ("{{ new_list_name }}".trim() == "") {
    if (localStorage.userEdits != null) {
      if (localStorage.userEdits.trim() == "") {
        localStorage.userEdits = "--";
      }
      document.getElementById("editable-list-name").innerText =
        localStorage.userEdits;
    }
  } else {
    localStorage.userEdits =
      document.getElementById("editable-list-name").innerText;
  }
}
