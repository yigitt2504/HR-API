const API_URL = "http://localhost:8000";
const API_KEY = "api_key123";
const PAGE_SIZE = 5;

let deptPage = 1;
let empPage = 1;

let deptMap = {};

function showLoading(id, show) {
    document.getElementById(id).style.display = show ? "block" : "none";
}

async function safeFetch(url, options = {}) {
    options.headers = options.headers || {};
    options.headers["x-api-key"] = API_KEY;

    const res = await fetch(url, options);

    if (!res.ok) {
        const text = await res.text();
        throw new Error(text || "İstek yerine getirilemedi!");
    }

    return res.json().catch(() => null);
}

/* Departmanlar
Departments */

async function loadDepartments() {
    try {
        showLoading("deptLoading", true);
        const skip = (deptPage - 1) * PAGE_SIZE;
        const depts = await safeFetch(`${API_URL}/departments?skip=${skip}&limit=${PAGE_SIZE}`);
        const tbody = document.querySelector("#deptTable tbody");
        tbody.innerHTML = "";

        depts.forEach(dept => {
            const deptRow = document.createElement("tr");
            deptRow.innerHTML = `
                <td>${dept.id}</td>
                <td><input value="${dept.name}" id="dept-name-${dept.id}" /></td>
                <td><input value="${dept.location || ""}" id="dept-location-${dept.id}" /></td>
                <td>
                    <button class="update-btn" onclick="updateDepartment(${dept.id})">Update</button>
                    <button class="delete-btn" onclick="deleteDepartment(${dept.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(deptRow);
        });

        document.getElementById("deptPageInfo").textContent = `Sayfa ${deptPage}`;

        await populateDepartmentDropdown();

    } catch (err) {
        alert("Departmanlar yüklenemedi");
        console.error(err);
    } finally {
        showLoading("deptLoading", false);
    }
}

async function populateDepartmentDropdown() {
    try {
        const depts = await safeFetch(`${API_URL}/departments?skip=0&limit=1000`);
        const select = document.getElementById("empDept");
        select.innerHTML = "";
        deptMap = {};

        depts.forEach(d => {
            const option = document.createElement("option");
            option.value = d.name;
            option.textContent = d.name;
            select.appendChild(option);
            deptMap[d.name] = d.name;
        });
    } catch (err) {
        console.error("Dropdown hatası:", err);
    }
}

async function updateDepartment(id) {
    try {
        const name = document.getElementById(`dept-name-${id}`).value;
        const location = document.getElementById(`dept-location-${id}`).value;

        if (!name || !location) return alert("Departman adı ve lokasyonu gerekli!");

        await safeFetch(`${API_URL}/departments/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, location })
        });

        loadDepartments();
    } catch (err) {
        alert("Departman güncellemesi başarısız!");
        console.error(err);
    }
}

async function deleteDepartment(id) {
    if (!confirm("Silmek istediğinize emin misiniz?")) return;
    try {
        await safeFetch(`${API_URL}/departments/${id}`, { method: "DELETE" });
        loadDepartments();
    } catch (err) {
        alert("Departman silinemedi");
        console.error(err);
    }
}

window.nextDeptPage = function() { deptPage++; loadDepartments(); };
window.prevDeptPage = function() { if (deptPage > 1) deptPage--; loadDepartments(); };

/* Çalışanlar 
Employees */

async function loadEmployees() {
    try {
        showLoading("empLoading", true);
        const skip = (empPage - 1) * PAGE_SIZE;
        const emps = await safeFetch(`${API_URL}/employees?skip=${skip}&limit=${PAGE_SIZE}`);
        const tbody = document.querySelector("#empTable tbody");
        tbody.innerHTML = "";

        emps.forEach(emp => {
            let deptOptions = "";
            for (const name of Object.values(deptMap)) {
                deptOptions += `<option value="${name}" ${name === emp.department_name ? "selected" : ""}>${name}</option>`;
            }

            const empRow = document.createElement("tr");
            empRow.innerHTML = `
                <td>${emp.id}</td>
                <td><input value="${emp.first_name}" id="emp-first-name-${emp.id}" /></td>
                <td><input value="${emp.last_name}" id="emp-last-name-${emp.id}" /></td>
                <td><input value="${emp.email}" id="emp-email-${emp.id}" /></td>
                <td><input type="number" value="${emp.salary}" id="emp-salary-${emp.id}" /></td>
                <td><input type="date" value="${emp.start_date}" id="emp-date-${emp.id}" /></td>
                <td>
                    <select id="emp-dept-${emp.id}">
                        ${deptOptions}
                    </select>
                </td>
                <td>
                    <button class="update-btn" onclick="updateEmployee(${emp.id})">Update</button>
                    <button class="delete-btn" onclick="deleteEmployee(${emp.id})">Delete</button>
                </td>
            `;
            tbody.appendChild(empRow);
        });

        document.getElementById("empPageInfo").textContent = `Sayfa ${empPage}`;

    } catch (err) {
        alert("Çalışanlar yüklenemedi!");
        console.error(err);
    } finally {
        showLoading("empLoading", false);
    }
}

async function updateEmployee(id) {
    try {
        const first_name = document.getElementById(`emp-first-name-${id}`).value;
        const last_name = document.getElementById(`emp-last-name-${id}`).value;
        const email = document.getElementById(`emp-email-${id}`).value;
        const salary = parseFloat(document.getElementById(`emp-salary-${id}`).value);
        const start_date = document.getElementById(`emp-date-${id}`).value;
        const dept_name = document.getElementById(`emp-dept-${id}`).value;

        if (!first_name || !email || isNaN(salary) || !last_name || !dept_name || !start_date)
            return alert("Bütün bilgilerin girilmesi gerekir!");

        if (!/^\S+@\S+\.\S+$/.test(email))
            return alert("Geçersiz email!");

        await safeFetch(`${API_URL}/employees/${id}`, {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_name,
                last_name,
                email,
                salary,
                start_date,
                department_name: dept_name
            })
        });

        loadEmployees();
    } catch (err) {
        alert("Güncellenemedi!");
        console.error(err);
    }
}

async function deleteEmployee(id) {
    if (!confirm("Silmek istediğine emin misin?")) return;
    try {
        await safeFetch(`${API_URL}/employees/${id}`, { method: "DELETE" });
        loadEmployees();
    } catch (err) {
        alert("Silinemedi!");
        console.error(err);
    }
}

window.nextEmpPage = function() { empPage++; loadEmployees(); };
window.prevEmpPage = function() { if (empPage > 1) empPage--; loadEmployees(); };

/* Formlar
Forms */

document.addEventListener("DOMContentLoaded", () => {

    document.getElementById("departmentForm").addEventListener("submit", async e => {
        e.preventDefault();
        const name = document.getElementById("deptName").value;
        const location = document.getElementById("deptLocation").value;

        if (!name || !location) return alert("Departman adı ve lokasyonu gerekli!");

        await safeFetch(`${API_URL}/departments`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, location })
        });

        e.target.reset();
        loadDepartments();
    });

    document.getElementById("employeeForm").addEventListener("submit", async e => {
        e.preventDefault();
        const first_name = document.getElementById("empFirstName").value;
        const last_name = document.getElementById("empLastName").value;
        const email = document.getElementById("empEmail").value;
        const salary = parseFloat(document.getElementById("empSalary").value);
        const dept_name = document.getElementById("empDept").value;
        const start_date = document.getElementById("empDate").value;

        if (!first_name || !email || isNaN(salary) || !dept_name || !last_name || !start_date)
            return alert("Eksik bilgi!");

        if (salary < 10000) return alert("Mümkün olmayan maaş değeri!");
        if (!/^\S+@\S+\.\S+$/.test(email)) return alert("Geçersiz email!");

        await safeFetch(`${API_URL}/employees`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                first_name,
                last_name,
                email,
                salary,
                start_date,
                department_name: dept_name
            })
        });

        e.target.reset();
        loadEmployees();
    });

    loadDepartments();
    loadEmployees();
});