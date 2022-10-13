#!/usr/bin/env python

def main():
    print("### Start")
    """
    S1:
        1 = se situa a si mismo
        0 = mueve a S2
    S2:
        1 = se situa a si mismo
        0 = mueve a S1
    Resumen: el estado debe terminar en S1 para ser correcto, S2 sera incorrecto
    """
    #myinput = [1, 0, 0, 1] # correcto
    #myinput = [1, 0] # incorrecto
    #myinput = [1, 0, 0, 0] # incorrecto
    myinput = [1, 0, 0, 0, 0] # correcto
    print("input:", myinput)

    inicio = 1
    finalizar = 1
    actual = 1
    #fin = False

    contador = 0
    #while fin==False:
    while contador!=len(myinput):
        print("## evaluando:", myinput[contador])
        print("contador:", contador)
        print("actual:", actual)
        if actual==1:
            if myinput[contador] == 1:
                actual=1
            if myinput[contador] == 0:
                actual=2
            contador+=1
            continue
        if actual==2:
            if myinput[contador] == 1:
                actual=2
            if myinput[contador] == 0:
                actual=1
            contador+=1
            continue
    if actual==finalizar:
        print("La cadena es correcta")
    else:
        print("La cadena es incorrecta")


if __name__=="__main__":
    main()
