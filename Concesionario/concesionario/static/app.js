"use strict"
let nombre = document.getElementById("id_nombre");
let apellido1 = document.getElementById("id_primer_apellido");
let apellido2 = document.getElementById("id_segundo_apellido");
let dni = document.getElementById("id_dni");

//let enviar=document.getElementById("enviar");
//let alerta=document.getElementById("errorFormulario");





window.addEventListener("load", () => {
	
	dni.addEventListener("blur", validarDni);
	nombre.addEventListener("focusout", validarNombre);
	apellido1.addEventListener("blur", validarApe1);
	apellido2.addEventListener("focusout", validarApe2);
	


})


function validarDni(){

 	
 	let expresion =/^\d{8}[a-zA-Z]{1}$/;
 	let spam = document.getElementById("errorDni"); 
 	if (!expresion.test(dni.value)) {
		spam.innerHTML = "Debe introducir un numero de ocho digitos seguido de una letra";
		dni.focus();
	} else{
		let numero;
		let letra;
		let clave;
		numero=dni.value.substr(0,dni.value.length-1);
		letra=dni.value.substr(dni.value.length-1,1);
		letra=letra.toUpperCase();
		numero=numero%23;
		clave="TRWAGMYFPDXBNJZSQVHLCKET";
		clave=clave.substring(numero,numero+1);
		if(clave!=letra){
			spam.innerHTML = "DNI incorrecto";
			dni.focus();
		}else{
			spam.innerHTML = "";
		}
	}
	
 }


function validarNombre(){
 	let expresion =/^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{2,20}$/;
 	let spam = document.getElementById("errorNombre"); 
 	if (!expresion.test(nombre.value)) {
		spam.innerHTML = "Debe introducir un nombre correcto";
		nombre.focus();
	} else{
		spam.innerHTML = "";
	}	
 }


 function validarApe1(){
 	let expresion =/^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{2,20}$/;
 	let spam = document.getElementById("errorPrimerApellido"); 
 	if (!expresion.test(apellido1.value)) {
		spam.innerHTML = "Debe introducir un apellido correcto";
		apellido1.focus();
	} else{
		spam.innerHTML = "";
	}	
 }


  function validarApe2(){
 	let expresion =/^[a-zA-ZÀ-ÿ\u00f1\u00d1\s]{2,20}$/;
 	let spam = document.getElementById("errorSegundoApellido"); 
 	if (!expresion.test(apellido2.value)) {
		spam.innerHTML = "Debe introducir un apellido correcto";
		apellido2.focus();
	} else{
		spam.innerHTML = "";
	}	
 }






