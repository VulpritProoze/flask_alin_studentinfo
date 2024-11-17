document.getElementById('image').src = imgDefaultSrc;

function editStudent(idno, lastname, firstname, course, level, image) {
	view_record(idno, lastname, firstname, course, level, image);
	showModal();
}

function addStudent() {
	showModal();
	document.getElementById('flag').value = 0;
    console.log(document.getElementById('flag').value);
	setModalFormAction();
}

function deleteStudent(idno) {
	document.getElementById('delete-student-input').value = idno;
}

function setModalFormAction() {
	const form = document.getElementById('modal-form');
	const flag = document.getElementById('flag').value;
	const action = (flag == '1') ? '/update_student' : '/add_student';
	form.action = action;
}

function cancelStudent() {
	hideModal();
	document.getElementById('image').src = imgDefaultSrc;
    document.getElementById('idno').value = '';
    document.getElementById('idno').readOnly = false;
    document.getElementById('lastname').value = '';
    document.getElementById('firstname').value = '';
    document.getElementById('course').value = '';
    document.getElementById('level').value = '';
    document.getElementById('flag').value = 0;
    console.log(document.getElementById('flag').value);	
}

function view_record(idno, lastname, firstname, course, level, image) {
    document.getElementById('image').src = image;
    document.getElementById('idno').value = idno;
    document.getElementById('idno').readOnly = true;
    document.getElementById('lastname').value = lastname;
    document.getElementById('firstname').value = firstname;
    document.getElementById('course').value = course;
    document.getElementById('level').value = level;
    document.getElementById('flag').value = 1;
    console.log(document.getElementById('flag').value);
    console.log("Update student image: ", document.getElementById('image').src);
    setModalFormAction();
}

function showModal() {
	let modal = document.getElementById('student-modal');
	modal.classList.remove('hidden');
	modal.classList.add('ease-out', 'duration-300', 'opacity-100');
	setTimeout(() => modal.classList.remove('opacity-0'), 200);
}

function hideModal() {
	let modal = document.getElementById('student-modal');
	modal.classList.add('ease-in', 'duration-200', 'opacity-0');
  	setTimeout(() => modal.classList.add('hidden'), 200);
}

function readURI(input) {
    if(input.files && input.files[0]){
        reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('image').src = e.target.result;
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function checkIfFieldsExists() {
    const idno = document.getElementById('idno').value.trim();
    const lastname = document.getElementById('lastname').value.trim();
    const firstname = document.getElementById('firstname').value.trim();
    const course = document.getElementById('course').value.trim();
    const level = document.getElementById('level').value.trim();
    const img = substringer(document.getElementById('image').src, "/static/img/");
    if (!idno || !lastname || !firstname || !course || !level) {
        alert("Please fill in all fields.");
        return false;
    }
    if (img == imgDefaultSrc) {
        alert("Please insert an image.");
        return false;
    } 
    console.log(img)
    console.log(imgDefaultSrc)
    return true;
}

function substringer(str, phrase) {
    const index = str.indexOf(phrase);
    str = (index !== -1) ? str.slice(index) : ''; 
    return str;
}