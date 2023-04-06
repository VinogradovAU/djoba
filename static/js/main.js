//модальное окно для вывода данных юзера по кнопке ИМЯ на джобе (на объявлении)
 var modalUserInfo = document.getElementById('modalUserInfo');

if (typeof(modalUserInfo) != 'undefined' && modalUserInfo != null)
{
	modalUserInfo.addEventListener('show.bs.modal', function (event) {
		  // Кнопка, запускающая модальное окно
		  var button = event.relatedTarget
		  // Извлечь информацию из атрибутов data-bs- *
		  var uuid_job = button.getAttribute('data-bs-jobuuid')

		  //modal_body это div в котрый мы поместим полученноую о юзере инфу в формате html
		  var modal_body = modalUserInfo.querySelector('.modal-body')
		  get_userinfo_from_server(uuid_job, modal_body)

		})
}
async function approved_performer(element_button){
	//функция срабатывает при нажатии кнопки "одобрить исполнитетя" - на конкретном юзере
	// в профиле юзера в списке откликнувшихся юзеров.
	var uuid_job = element_button.getAttribute('uuid_job');
	var user_id = element_button.getAttribute('user_id');
	var text_status = document.querySelector('.card-status-' + user_id);
	url = '/jobs/booking/approved/' + uuid_job + "/" + user_id;
	let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
        // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        // {'error': None, 'booking_status': '89260000000'}
            let json = await response.json();
            console.log("json: ", json);
			if (json['code']=='E001'){
                console.log("approved_performer_status:", json['approved_performer_status']);
                text_status.innerText = 'Исполнителю отправлено сообщение';
                }
        } else {
            text_status.innerText = 'Ошибка сервера. Обратитесь к администратору';
            console.log("Ошибка HTTP: " + response.status);
        }

}

async function toogle_view_job(element_button){
	var uuid_job = element_button.getAttribute('jobuuid');
	var views_div = document.querySelector('.view-job-'+uuid_job);
	if(views_div.classList.contains("view-job-style")) {
          views_div.classList.remove('view-job-style');
     } else {
          views_div.classList.add('view-job-style');
     }
}
async function set_booking_jobuuid(element_button){
//	var uuid_job = element_button.getAttribute('jobuuid');
	var getphone_button = document.querySelector('.get-phone');
	var uuid_job = getphone_button.getAttribute('jobuuid');
	url = '/jobs/set_booking/' + uuid_job;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
        // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        // {'error': None, 'booking_status': '89260000000'}
            let json = await response.json();
            console.log("json: ", json);
            if (json['code']=='E003'){
                console.log("booking_status:", json['booking_status']);
                phone_path.innerText = 'Заявка создана. Автор заявки получит сообщение.';
                }
            if (json['code']=='E001' || json['code']=='E002' ||json['code']=='E006'){
                console.log("error:", json['error']);
                phone_path.innerText = json['error']; // заявка подана ранее
                }
            if (json['code']=='E004' || json['code']=='E005'){
                phone_path.innerText = 'Не удалось забронировать джобу. Обратитесь к администратору';
                console.log("error: ", json['error']);
            }

        } else {
            phone_path.innerText = 'Не удалось забронировать джобу. Обратитесь к администратору';
            console.log("Ошибка HTTP: " + response.status);
        }
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

function generate_stars(rait_num){
	val_rait = rait_num;
	if (val_rait == null) {
        val_rait = "0.0";
    }
	if (val_rait == "") {
        val_rait = "0.0";
    }
    rait_html = '';
    rait_html = rait_html + '<h3>' + val_rait + '</h3>';

    rait = val_rait.split(".");
    flag = 0;

    if (rait[0] == 0 && rait[1] == 0) {
        //все звезды пустые
        star_num = rait[1];
        for (x = 1; x <= 5; x++) {
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-' + star_num + '.png"></div></div>'
        }
        flag = 1;
    }
    if (rait[0] == 0 && rait[1] > 0 && flag == 0) {
        //одна звезда частично, остальныепустые
        star_num = 0;
        rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-0' + rait[1] + '.png"></div></div>'
        for (x = 1; x <= 4; x++) {
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-' + star_num + '.png"></div></div>'
        }
        flag = 1;
    }

    if (rait[0] > 0 && rait[1] >= 0 && flag == 0) {
        //одна звезда частично, остальныепустые
        star_num = 10;
        for (x = 1; x <= rait[0]; x++) {
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-' + star_num + '.png"></div></div>'
        }

        if (rait[1] == 0) {
            star_num = 0;
            aa = 5 - rait[0]
            for (x = 1; x <= aa; x++) {
                rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-' + star_num + '.png"></div></div>'
            }
        } else {
            star_num = rait[1];
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-0' + star_num + '.png"></div></div>'
            star_num = 0;
            ss = 5 - rait[0] - 1;
            for (x = 1; x <= ss; x++) {
                rait_html = rait_html + '<div class="wrapper exmpl"><div><img src="/static/images/star-' + star_num + '.png"></div></div>'
            }
            flag = 1;
        }
    }
return rait_html
}


async function get_userinfo_from_server(uuid_job, modal_body){
        url = '/userinfo/' + uuid_job;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
        // если HTTP-статус в диапазоне 200-299
        // получаем тело ответа (см. про этот метод ниже)
        // {'error': None,
        //'user_name': 'user_name', 'user_phone':'user_phone',
        //'user_email':'user_email', 'user_rait':'user_rait'}

	            let json = await response.json();

	            if (json) {
	                let err = 0

					if (json['user_banned']==false || json['user_banned']==true){
		                console.log('user_banned is ok')
		            } else {console.log('user_banned is ERROR'); err = 1}

		            if (json['user_name']!=''){
		                console.log('user_name is ok')
		            }else {console.log('user_name is ERROR'); err = 1}

		            if (json['error']!=''){
		                console.log('error is ok')
		            }else {console.log('error is ERROR'); err = 1}

		            if (json['user_phone']!=''){
		                console.log('user_phone is ok')
		            }else {console.log('user_phone is ERROR'); err = 1}

		            if (json['user_email']!=''){
		                console.log('user_email is ok')
		            }else {console.log('user_email is ERROR'); err = 1}

		            if (json['user_rait']!=''){
		                console.log('user_rait is ok')
		                rait=json['user_rait'];
		            }else {
		            console.log('user_rait is ERROR');
		            err = 1;
		            rait="0.0"}

					  //ТУТ функция запроса к бэку и возврат уже готового куска HTML
					info_html=''
					if (err==1) {
					  info_html = '<h2>Не удалось получить данные о пользователе. Обратитесь к администратору</h2>'

					} else {
					  info_html = info_html + '<div class="card>"'+
								'<ul class="list-group list-group-flush">'+
							    '<li class="list-group-item list-background-color">Имя: '+ json['user_name'] + '</li>'+
							    '<li class="list-group-item list-background-color">Тел.: '+ json['user_phone'] + '</li>'+
							    '<li class="list-group-item list-background-color">Email: '+ json['user_email'] + '</li>'+
							    '</ul></div>'
					  info_html = info_html + '<div class="row">' +
			            '<div class="col">' +
			                '<div class="row rait_row">'
			                + generate_stars(rait) +
			                '</div>'+
			            '</div>'+
			        '</div>'
					}
			        modal_body.innerHTML = info_html

		        } else {
		          info_html = '<h2>Не удалось получить данные о пользователе. Обратитесь к администратору</h2>'
				  modal_body.innerHTML = info_html
		        }

        } else {
            console.log("Ошибка HTTP: " + response.status);
            info_html = '<h2>Не удалось получить данные о пользователе. Обратитесь к администратору</h2>'
            modal_body.innerHTML = info_html
        }

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
                    phone_path.innerHTML = '<a class="btn btn-primary" href="/auth/login" role="button">Нажмите чтобы войти</a>'
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