const API_URL = 'http://localhost:5000';

document.addEventListener("DOMContentLoaded", () => {
    fetchUsers();

    document.getElementById("userForm").addEventListener("submit", function (e) {
        e.preventDefault();
        const id = document.getElementById("userId").value;
        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const dob = document.getElementById("dob").value;

        const user = { name, email, dob };

        if (id) {
            fetch(`${API_URL}/user/${id}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            }).then(() => fetchUsers());
        } else {
            fetch(`${API_URL}/user`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(user)
            }).then(() => fetchUsers());
        }
        this.reset();
    });
});

function fetchUsers() {
    fetch(`${API_URL}/users`)
        .then(res => res.json())
        .then(data => {
            const usersList = document.getElementById("usersList");
            usersList.innerHTML = '';
            data.forEach(user => {
                usersList.innerHTML += `
                    <div>
                        <strong>${user.name}</strong> (${user.email}, ${user.dob})
                        <button onclick="editUser(${user.id}, '${user.name}', '${user.email}', '${user.dob}')">Edit</button>
                        <button onclick="deleteUser(${user.id})">Delete</button>
                    </div>
                `;
            });
        });
}

function editUser(id, name, email, dob) {
    document.getElementById("userId").value = id;
    document.getElementById("name").value = name;
    document.getElementById("email").value = email;
    document.getElementById("dob").value = dob;
}

function deleteUser(id) {
    fetch(`${API_URL}/user/${id}`, {
        method: 'DELETE'
    }).then(() => fetchUsers());
}
