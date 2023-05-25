//дожидаемся полной загрузки страницы
async function generate_stars_on_history_list(rait_num){
	val_rait = rait_num;
	if(val_rait.length == 1){
		val_rait=val_rait+".0";
	}
	if (val_rait == null) {
        val_rait = "0.0";
    }
	if (val_rait == "") {
        val_rait = "0.0";
    }
    rait_html = '';
    rait_html = rait_html + '<h6>' + val_rait + '</h6>';

    rait = val_rait.split(".");
    flag = 0;

    if (rait[0] == 0 && rait[1] == 0) {
        //все звезды пустые
        star_num = rait[1];
        for (x = 1; x <= 5; x++) {
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-' + star_num + '.png"></div></div>'
        }
        flag = 1;
    }
    if (rait[0] == 0 && rait[1] > 0 && flag == 0) {
        //одна звезда частично, остальныепустые
        star_num = 0;
        rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-0' + rait[1] + '.png"></div></div>'
        for (x = 1; x <= 4; x++) {
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-' + star_num + '.png"></div></div>'
        }
        flag = 1;
    }

    if (rait[0] > 0 && rait[1] >= 0 && flag == 0) {
        //одна звезда частично, остальныепустые
        star_num = 10;
        for (x = 1; x <= rait[0]; x++) {
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-' + star_num + '.png"></div></div>'
        }

        if (rait[1] == 0) {
            star_num = 0;
            aa = 5 - rait[0]
            for (x = 1; x <= aa; x++) {
                rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-' + star_num + '.png"></div></div>'
            }
        } else {
            star_num = rait[1];
            rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-0' + star_num + '.png"></div></div>'
            star_num = 0;
            ss = 5 - rait[0] - 1;
            for (x = 1; x <= ss; x++) {
                rait_html = rait_html + '<div class="wrapper exmpl"><div><img style="width: 50%;" src="/static/images/star-' + star_num + '.png"></div></div>'
            }
            flag = 1;
        }
    }
return rait_html
}

async function getStars_by_Jobuuid_and_User_Id(jou_uuid, user_id){
		stars = "4.2";
		return stars
}


window.onload = async function () {
	var all_card_with_stars = document.querySelectorAll('.stars_pic');
	for(elem=0; elem < all_card_with_stars.length; elem++){
		rait = all_card_with_stars[elem].getAttribute('value_rait');
		job_uuid = all_card_with_stars[elem].getAttribute('value_job_uuid');
		user_uuid = all_card_with_stars[elem].getAttribute('value_user_uuid');

		url = '/jobs/star/' + user_uuid + '/'+ job_uuid;
        let response = await fetch(url);
        console.log("response.ok", response.ok);
        console.log("response.status", response.status);
        if (response.ok) {
         let json = await response.json();
         console.log("json: ", json);
          rait = json['rait'];
          console.log('rait= '+rait);
        } else {
          console.log("Ошибка HTTP: " + response.status);
        }
        if (rait!='None'){
		info_html = '';
//		info_html = info_html + '<div class="row">';
//		info_html = info_html + '<div class="col-3"> ';
//		info_html = info_html + 'Ваша оценка: ';
//		info_html = info_html + '</div>';
		info_html = info_html + '<div class="col">';
		info_html = info_html + 'Ваша оценка: ';
		info_html = info_html + '<div class="row rait_row_min">';
		info_html = info_html + await generate_stars_on_history_list(rait);
		info_html = info_html +'</div>';
		info_html = info_html +'</div>';
//		info_html = info_html +'</div>';
		all_card_with_stars[elem].innerHTML=info_html
		}
	}

}