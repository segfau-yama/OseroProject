
#include <stdio.h>
#include <WinSock2.h>
#include <stdlib.h>
#include <string.h>
#include <io.h>

#define RCVBUFSIZE 32
#define B_size 10
#define R_size 1024

#pragma comment(lib, "Ws2_32.lib")

void DieWithError(char *errorMessage);
void Othello(int sock);
void output(int **Buffer);     //画面出力
void send_serv(int sock);       //サーバーに送信
//下二つが文字列を分割するsplit関数とそれに用いるユーザ関数
int  isDelimister(char p,char delim);
void split(char *dst[],char *src,char delim);

int main(int argc, char *argv[]){
  int sock;                        // ソケットディスクリプタ
  struct sockaddr_in echoServAddr; // サーバーアドレスを格納
  unsigned short echoServPort;     // ポート番号を格納
  char *servIP;                    // サーバーのIPアドレスを格納

	WSADATA wsa_data;

  if (argc < 2){
    fprintf(stderr, "%s：コマンドの後に<Server IP>を入力して下さい。\n", argv[0]);
    exit(1);
  }

  servIP = argv[1];       // ここ？
  echoServPort = 12345;   // ここ？

	WSAStartup(MAKEWORD(2, 2), &wsa_data);

  if ((sock = socket(PF_INET, SOCK_STREAM, IPPROTO_TCP)) < 0)
      DieWithError("socket() failed");

  /* Construct the server address structure */
  memset(&echoServAddr, 0, sizeof(echoServAddr));     /* Zero out structure */
  echoServAddr.sin_family      = AF_INET;             /* Internet address family */
  echoServAddr.sin_addr.s_addr = inet_addr(servIP);   /* Server IP address */
  echoServAddr.sin_port        = htons(echoServPort); /* Server port */

  /* Establish the connection to the echo server */
  if (connect(sock, (struct sockaddr *) &echoServAddr, sizeof(echoServAddr)) < 0)
      DieWithError("connect() failed");

  // 対戦の処理
  Othello(sock);

  //close(sock);
  closesocket(sock);
  exit(0);
}


void Othello(int sock){
    int **Buffer = calloc(B_size, sizeof(int *));     // データを2次元配列に変換したものを格納
    char rBuffer[R_size];
    int state;                       // 先攻か後攻か試合終了か制御
    char *dst[110];                  // 分割した文字列を格納する配列へのポインタ
    int turn;                        //手番を格納する
    int result;                      //勝敗

    for(int i=0; i<B_size; i++)
      Buffer[i] = calloc(B_size, sizeof(int));

    printf("Start: \n");             /* 対戦開始 */

    while (1)
    {
        memset(Buffer, 0, sizeof(Buffer));
        memset(rBuffer, 0, sizeof(rBuffer));
        recv(sock, rBuffer, R_size-1, 0);

        switch(rBuffer[0]){
          case 3:
            split(dst,rBuffer,',');
            turn=atoi(dst[1]);
            for(int i=0;i<B_size;i++){
              for(int j=0;j<B_size;j++){
                int k=10*i+j+2;
                Buffer[i][j]=atoi(dst[k]);
              }
            }
            output(Buffer);
            if(state == turn%2){
              printf("牌を置きたい座標を「縦 横」で入力して下さい。\n");
              send_serv(sock);
            }
            break;

          case 4:
            split(dst,rBuffer,',');
            result=atoi(dst[1]);
            /*
            dst[2]...黒のコマの枚数
            dst[3]...白のコマの枚数
            */
            if( (result==0 && turn==2) || (result==1 && turn==3) )
                printf("You win!\n");
            else if( (result==0 && turn==3) || (result==1 && turn==2) )
                printf("You lose...\n");
            else
                printf("Draw\n");
            printf("黒のコマ：%c\n", dst[2]);
            printf("白のコマ：%c\n", dst[3]);
            break;

          case 5:
            split(dst,rBuffer,',');
            state=atoi(dst[1]);
            turn=atoi(dst[2]);
            for(int i=0;i<B_size;i++){
              for(int j=0;j<B_size;j++){
                int k=10*i+j+3;
                Buffer[i][j]=atoi(dst[k]);
              }
            }
            output(Buffer);
            if(state == turn%2){
              printf("牌を置きたい座標を「縦 横」で入力して下さい。\n");
              send_serv(sock);
            }
            break;

          case 6:
            printf("そこには置けません。もう一度座標を入力して下さい。\n");
            send_serv(sock);
            break;

        }

    }

    for(int i=0; i<B_size; i++)
      free(Buffer[i]);
    free(Buffer);

    printf("\n");    /* Print a final linefeed */

}


void output(int **Buffer){
  printf("盤面\n");
  printf("  1 2 3 4 5 6 7 8\n");

  for(int i=1; i<(B_size-1); i++){
    printf("%d", i);

    for(int j=1; j<(B_size-1); j++)
      switch(Buffer[i][j]){
        case 0:
          printf(" *");
          break;
        case 1:
          printf(" ●");
          break;
        default:
          printf(" ○");
          break;
      }

    printf("\n");
  }

}


void send_serv(int sock){
  int low, col;      // 縦、横の座標を格納
  char *echoString;  // サーバーに送る用

  scanf("%d %d", &low, &col);
  while( (low<'1'&&'8'<low) || (col<'1'&&'8'<col) ){
    printf("そこには置けません。もう一度座標を入力して下さい。\n");
    scanf("%d %d", &low, &col);
  }
  sprintf(echoString, "%d %d", col--, low--);
  send(sock, echoString, strlen(echoString), 0);

}


int isDelimiter(char p,char delim){
  return p==delim;
}


void split(char *dst[],char *src,char delim){
  int c=0;

  for(;;){
    while(isDelimiter(*src,delim)){
      src++;
    }

    if(*src=='\0'){
      break;
    }

    dst[c++]=src;

    while(*src &&!isDelimiter(*src,delim)){
      src++;
    }

    if(*src=='\0'){
      break;
    }

    *src++='\0';
  }

}
