function setDueDate(date_data, task_id) {
  $.ajax({
    url: '{{ url_for("task_lists") }}',
    method: "POST",
    data: {
      name: date_data,
      task_id: task_id,
    },
  });
}
function deleteTask(task_id, task_index) {
  $.ajax({
    url: '{{ url_for("task_lists") }}',
    method: "POST",
    data: {
      delete_task_id: task_id,
    },
  });
  let deleted_container =
    document.getElementsByClassName("task-container")[task_index - 1];
  deleted_container.style.display = "none";
}
function setAlert(index, task_id) {
  let alertBtnValue =
    document.getElementsByClassName("alert-time-picker")[index - 1].value;
  $.ajax({
    url: '{{ url_for("set_alert")}}',
    method: "POST",
    data: {
      alertDateTime: alertBtnValue,
      taskId: task_id,
    },
  });
}
