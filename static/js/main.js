//модальное окно для вывода данных юзера по кнопке ИМЯ на джобе (на объявлении)
 var modalUserInfo = document.getElementById('modalUserInfo');

if (typeof(modalUserInfo) != 'undefined' && modalUserInfo != null)
{
	modalUserInfo.addEventListener('show.bs.modal', function (event) {
		  // Кнопка, запускающая модальное окно
		  var button = event.relatedTarget
		  // Извлечь информацию из атрибутов data-bs- *
		  var jobauuid = button.getAttribute('data-bs-jobuuid')

		  //modal_body это div в котрый мы поместим полученноую о юзере инфу в формате html
		  var modal_body = modalUserInfo.querySelector('.modal-body')

		  //ТУТ функция запроса к бэку
		  modal_body.innerHTML = '<h2>ТУТ инфа о юзере с UUID объявления: '+ jobauuid+'</h2>'
		  modal_body.innerHTML = info_html

		})
}

var phone_path = document.querySelector('.phone-path')
async function get_phone_from_jobuuid(element_button){
	var uuid_job = element_button.getAttribute('jobuuid');
//	console.log('uuid_job:' + uuid_job);
	get_phone_from_server(uuid_job);
//	phone_path.innerText = "запросим у сервера и получим номер";
}

//пот вызове модального окна, с кнопки вызова берется uuid джобы и
//пишется в атрибут кнопки показа телефонного номера.
//этот uuid нужет при нажатии кнопки - "показать телефон" для запроса не сервер


    var exampleModal = document.getElementById('exampleModal');

if (typeof(exampleModal) != 'undefined' && exampleModal != null)
{
		  exampleModal.addEventListener('show.bs.modal', function (event) {
		  // Кнопка, запускающая модальное окно
		  var button = event.relatedTarget
		  // Извлечь информацию из атрибутов data-bs- *
		  var jobuuid = button.getAttribute('data-bs-jobuuid')
		  var title = button.getAttribute('title')
		  // При необходимости вы можете инициировать запрос AJAX здесь
		  // а затем выполните обновление в обратном вызове.
		  //
		  // Обновите содержимое модального окна.
		  var modalTitle = exampleModal.querySelector('.modal-title')
		//  var modalBodyInput = exampleModal.querySelector('.modal-body input')

		  modalTitle.textContent = title
		  var button_get_phone = exampleModal.querySelector('.get-phone')
		  button_get_phone.setAttribute('jobuuid', jobuuid)
		//  modalBodyInput.value = recipient
		  phone_path.innerText = ""; //очищаю поле с телефоном
		})

}


async function get_phone_from_server(uuid_job){
        url = '/jobs/get_phone/' + uuid_job;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
        // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        // {'error': None, 'phone': '89260000000'}
            let json = await response.json();
            console.log("json: ", json);
            if (json['phone']!='' && json['error'] == 'None'){
            console.log("Получен номер телефона:", json['phone'])
            phone_path.innerHTML = '<h2>' + json['phone'] + '</h2>';
            }else {
                if (json['error']==401){
                    phone_path.innerHTML = '<a class="btn btn-primary" href="/auth/login" role="button">Нажмине чтобы войти</a>'
                } else {
                    phone_path.innerText = 'Ошибка ' + json['error'];
                }
                console.log("error: ", json['error']);
            }

        } else {
            phone_path.innerText = 'Не удалось получить номер. Обратитесь к администратору';
            console.log("Ошибка HTTP: " + response.status);
        }

}

async function deactivate_user(num_id){
        url = '/auth/deactivate/' + num_id;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
        // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        // {'error': None, 'status_banned': True}
        let json = await response.json();
        console.log("json: ", json);
          if (json['status_banned']=='True'){ console.log("Статус пользователя: Заблокирован")}
          if (json['status_banned']=='False'){ console.log("Статус пользователя: Активный")}
          if (json['status_banned']=='None'){ console.log("Не удалось получить статус пользователя")}

          console.log("error: ", json['error']);
        } else {
          console.log("Ошибка HTTP: " + response.status);
        }
}

async function activate_user(num_id){
        url = '/auth/activate/' + num_id;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
        // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        // {'error': None, 'status_banned': True}
        let json = await response.json();
         console.log("json: ", json);
          if (json['status_banned']=='True'){ console.log("Статус пользователя: Заблокирован")}
          if (json['status_banned']=='False'){ console.log("Статус пользователя: Активный") }
          if (json['status_banned']=='None'){ console.log("Не удалось получить статус пользователя")}

          console.log("error: ", json['error']);
        } else {
          console.log("Ошибка HTTP: " + response.status);
        }
}

/*функция делает отправляет запрос на сервер - снять с публикации джобу*/
async function publish_job_off(element){
		uuid_job = element.attributes.uuid_job.value;
        url = '/jobs/publishoff/' + uuid_job;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
         let json = await response.json();
         console.log("json: ", json);
          if (json['status_publishoff']=='True'){
          console.log("Джоба снята с публикации");
              var data_info_header = document.querySelector('.clear_data_' + uuid_job)
              data_info_header.innerHTML="";

	          var elem = document.querySelector('.job_status_' + uuid_job);
	          elem.innerText = 'ЧЕРНОВИК!';
	          elem.classList.remove('alert-success');
		      elem.classList.add('alert-primary');

		      element.classList.remove('btn-warning');
		      element.classList.add('btn-success');
		      element.innerText = "Опубликовать";
		      element.attributes.value.value = 'publishon';
          }
          if (json['status_publishoff']=='False'){ console.log("Не удалось снять джобу с публикации") }
          console.log("error: ", json['error']);
        } else {
          console.log("Ошибка HTTP: " + response.status);
        }
}


async function publish_job_change(element){
		uuid_job = element.attributes.uuid_job.value;
		value = element.attributes.value.value;
		if (value =='publishoff') {
			publish_job_off(element);
		} else {
			url = '/jobs/publishon/' + uuid_job;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
         let json = await response.json();
         console.log("json: ", json);
          if (json['status_publishon']=='True'){
          console.log("Джоба опубликована");
              var data_info_header = document.querySelector('.clear_data_' + uuid_job)
              data_info_header.innerHTML='<h5>' + data_info_header.getAttribute("value") + '</h5>';
              var elem = document.querySelector('.job_status_' + uuid_job);
	          elem.innerText = 'Объявление опубликовано!';
	          elem.classList.remove('alert-primary');
		      elem.classList.add('alert-success');

		      element.classList.remove('btn-success');
		      element.classList.add('btn-warning');
		      element.innerText = "Снять с публикации";
		      element.attributes.value.value = 'publishoff';
          }
          if (json['status_publishon']=='False'){ console.log("Не удалось опубликовать джобу") }
          console.log("error: ", json['error']);
        } else {
          console.log("Ошибка HTTP: " + response.status);
        }

		}

}


//дожидаемся полной загрузки страницы
window.onload = function () {

	function find_lable(find_num_id){
	var my_label = document.querySelectorAll('.activation_label');
	for (var i = 0; i < my_label.length; i++) {
	    num_id = my_label[i].getAttribute('num_id');
	    if (num_id==find_num_id){
	        return my_label[i]
	    }
	  };
	}

    var allButtons = document.querySelectorAll('.activation');

	for (var i = 0; i < allButtons.length; i++) {
	  item = allButtons[i]
	  item.addEventListener('click', function() {
	    console.clear();
	    num_id = this.getAttribute('num_id');
	    value = this.value;
	    console.log("You clicked:", value);
	    console.log("You clicked:", num_id);
		my_button = this
	    activ_button_onclick(my_button, num_id, value);
	  });
	}

	    function activ_button_onclick(my_button, num_id, value) {
	        //производим какие-то действия
//	        num_id = activ_button.getAttribute('num_id');
//	        value = activ_button.getAttribute('value');
			activation_label=find_lable(num_id);

			if (value=='deactive'){
			//нужно разблокировать юзера
			deactivate_user(num_id);

			activation_label.innerText = 'Заблокирован';
			activation_label.style.color = 'red';

			my_button.innerText = 'Разблокировать'
			my_button.classList.remove('btn-outline-danger');
	        my_button.classList.add('btn-outline-success');
			my_button.value='active'
			} else {

			if (value=='active')
			//нужно заблокировать юзера
			activate_user(num_id);

			activation_label.innerText = 'Активный';
			activation_label.style.color = 'green';

			my_button.innerText = 'Заблокировать'
			my_button.classList.remove('btn-outline-success');
	        my_button.classList.add('btn-outline-danger');
			my_button.value='deactive'
			}
	        return false;
	    }
}