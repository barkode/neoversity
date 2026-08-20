.data
msg db 'Hello, world!',0dh,0ah,'$'

.code
main proc
    mov ah, 09h
    lea dx, msg
    int 21h
    mov ax, 4c00h
    int 21h
main endp
end main
