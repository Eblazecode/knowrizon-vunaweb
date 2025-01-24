"use strict";

$("#swal-1").click(function () {
  swal('Hello');
});

$("#swal-2").click(function () {
  swal('Good Job', 'You clicked the button!', 'success');
});



$("#swal-3").click(function (event) {
  event.preventDefault();

  const formData = new FormData(document.getElementById('student_form_new'));
  const data = {};
  formData.forEach((value, key) => {
    data[key] = value;
  });

  const csrfToken = formData.get('csrfmiddlewaretoken');
  if (!csrfToken) {
    swal('Error', 'CSRF token missing. Please try again.', 'error');
    return;
  }




  fetch("/add_students/", {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-CSRFToken': csrfToken,
  },
  body: JSON.stringify(data),
})
.then((response) => {
  if (!response.ok) {
    throw new Error('Network response was not ok');
  }
  return response.json();
})
.then((data) => {
  if (data.status === "error") {
    swal('Error', data.message, 'error');
  } else {
    swal('Success', data.message, 'success').then(() => {
      window.location.href = "/admin_login/";
    });
  }
})
.catch((error) => {
  console.error('Error:', error);
  swal('Error', 'An unexpected error occurred.', 'error');
});
});

$("#swal-4").click(function () {
  swal('Good Job', 'You clicked the button!', 'info');
});

$("#swal-5").click(function () {
  swal('Good Job', 'You clicked the button!', 'error');
});

$("#swal-6").click(function () {
  swal({
    title: 'Are you sure?',
    text: 'Once deleted, you will not be able to recover this imaginary file!',
    icon: 'warning',
    buttons: true,
    dangerMode: true,
  })
    .then((willDelete) => {
      if (willDelete) {
        swal('Poof! Your imaginary file has been deleted!', {
          icon: 'success',
        });
      } else {
        swal('Your imaginary file is safe!');
      }
    });
});

$("#swal-7").click(function () {
  swal({
    title: 'What is your name?',
    content: {
      element: 'input',
      attributes: {
        placeholder: 'Type your name',
        type: 'text',
      },
    },
  }).then((data) => {
    swal('Hello, ' + data + '!');
  });
});

$("#swal-8").click(function () {
  swal('This modal will disappear soon!', {
    buttons: false,
    timer: 3000,
  });
});