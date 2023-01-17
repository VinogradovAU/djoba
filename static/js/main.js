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