let tasks_html;
let task_form;
let delete_all_done;
const url = 'http://localhost:8000'

document.addEventListener('DOMContentLoaded', () => {
    tasks_html = document.getElementById('Tasks');
    task_form = document.getElementById('make_task');
    delete_all_done = document.getElementById('delete_tasks_done')
    loadTasks();

    task_form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const textin = document.getElementById("textin");
        const title = textin.value;

        await fetch(url + '/tasks?title=' + title, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ title })
        });

    textin.value = ''
    loadTasks();
    })

    tasks_html.addEventListener('click', async (e) => {
        e.preventDefault();

        if (e.target.classList.contains('complete')) {
            const task_id = e.target.parentElement.dataset.id;
            await fetch(url + `/tasks/${task_id}`, {
                method: 'PATCH'
            })
            loadTasks();
        }
        else if (e.target.classList.contains('delete')) {
            const task_id = e.target.parentElement.dataset.id;
            await fetch(url + `/tasks/${task_id}`, {
                method: 'DELETE'
            })
            loadTasks();
        }

    })

    delete_all_done.addEventListener('click', async (e) => {
        e.preventDefault();
        await fetch(url + '/completed', {
                method: 'DELETE'
            })
            
            loadTasks();

    })
});

async function loadTasks() {
    response = await fetch(url + '/tasks');
    tasks = await response.json();

    tasks_html.innerHTML = '';

    tasks.forEach(task => {
        const button_complete = task.is_done ? '' : '<button class="complete">Complete</button>'
        const complete_text = task.is_done ? '' : 'complete'
        html_task = `<li class="${complete_text}" data-id="${task.id}"><span>${task.title}</span>${button_complete}<button class="delete">Delete</button></li>`;
        tasks_html.insertAdjacentHTML('beforeend', html_task);
    });
}

