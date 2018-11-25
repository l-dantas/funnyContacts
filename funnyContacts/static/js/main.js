
// Components Conluídos

// Script para aumentar e dinumuir o label dos inputs das telas de login e create pass
$('input[type="password"]').focus((e) => {
	$('label[for='+e.target.id+']').css({
		'top':'10px',
		'font-size':'10px'
	});
}).focusout((e) => {
	if(e.target.value){
		return;
	}
	$('label[for='+e.target.id+']').css({
		top:'40px',
		fontSize:'14px',
	});
});

// desabilitando o autocomplete de todos os input
$('input').attr('autocomplete','off');

// Sistema de busca 
$('.search-contact').keyup(() => {
	let text_search = $('.search-contact').val();
	// console.log(text_search.length);

	if(text_search.length > 0) {
		$('.contact').each((index) => {
			let h6 = $('.contact:eq('+ index +') > main h6');

			if(h6.text().slice(0, text_search.length).toLowerCase() === text_search.toLowerCase()){
				$('.contact:eq('+ index +')').show('slow');
			} else {
				$('.contact:eq('+ index +')').hide('slow');
			}
		});
	} else {
		$('.contact').show('slow');
	}
});

// components dos contatos
$('.contact main').hide();
$('.contact').hover((event) => {

	let main = event.currentTarget.children[1];
	$(main).show("slow",()=>{});

},(event) => {
	
	let main = event.currentTarget.children[1];
	$(main).hide("slow",()=>{});

});


// Components em DESENVOLVIMENTO


// Menu mobile - EM DESENVOLVIMENTO
// let widthWindow = $(document).innerWidth(() => {
// 	alert($(this).width());
// });
// if(widthWindow < 570){
// 	console.log(widthWindow);
// }


//Ordenando por A-Z - EM DESENVOLVIMENTO
$('#sort-AZ').click((event) => {

	let sort_abc = $('#sort-AZ');
	let contacts = $('.contact > main .contact-name ');

	if(sort_abc.text() === 'A-Z'){
		sort_abc.text('Z-A');
	} else {
		sort_abc.text('A-Z');
	}

	event.preventDefault();

});



//ocultar ou exibir os links de sort - EM DESENVOLVIMENTO
$('.links-sort').hide();
$('.area-error > article').hide();
$('.btn-sort').click(() => {
	alert('Sorry, this function isn\'t still done.');
	// $('.links-sort').toggle();
	$('.area-error > article').text('Sorry, this function isn\'t still done.');
	
});





