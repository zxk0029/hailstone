package main

import (
	"context"
	// "fmt" // Removed unused import
	"log"
	"time"

	account "github.com/hashkey/golan/proto/account"

	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

const (
	serverAddr = "43.154.95.45:30008" // Account Service Address
)

func main() {
	// --- 连接 gRPC 服务器 ---
	// 使用不安全凭证 (用于测试，生产环境应使用 TLS)
	conn, err := grpc.Dial(serverAddr, grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatalf("无法连接: %v", err)
	}
	defer conn.Close() // 确保连接关闭

	log.Printf("已连接到 %s", serverAddr)

	// --- 创建 Account 服务客户端 ---
	client := account.NewWalletAccountServiceClient(conn)

	// --- 准备请求 ---
	ctx, cancel := context.WithTimeout(context.Background(), time.Second*10) // 设置 10 秒超时
	defer cancel()

	req := &account.TxHashRequest{
		Chain:   "Ethereum",
		Network: "mainnet",
		Coin:    "ETH", // 从 symbol 推断
		Hash:    "0x7ead65088e31d94ef78ddc55a61870c31903f53b7b2a36808cec87dbc2a9d6ed",
		// consumer_token 如果需要，也在这里添加
	}

	log.Printf("发送请求: %v", req)

	// --- 调用 GetTxByHash ---
	resp, err := client.GetTxByHash(ctx, req)
	if err != nil {
		log.Fatalf("调用 GetTxByHash 失败: %v", err)
	}

	// --- 打印原始响应 ---
	log.Printf("收到响应 Code: %s", resp.GetCode())
	log.Printf("收到响应 Msg: %s", resp.GetMsg())
	if resp.GetTx() != nil {
		log.Printf("收到响应 Tx Hash: %s", resp.Tx.GetHash())
		log.Printf("收到响应 Tx Index: %d", resp.Tx.GetIndex())
		log.Printf("收到响应 Tx From: '%s'", resp.Tx.GetFrom()) // 直接打印 From 字段
		log.Printf("收到响应 Tx To: '%s'", resp.Tx.GetTo())
		log.Printf("收到响应 Tx Value: '%s'", resp.Tx.GetValue())
		log.Printf("收到响应 Tx Fee: %s", resp.Tx.GetFee())
		log.Printf("收到响应 Tx Status: %s (%d)", resp.Tx.GetStatus(), resp.Tx.GetStatus()) // 打印枚举名称和值
		log.Printf("收到响应 Tx Type: %d", resp.Tx.GetType())
		log.Printf("收到响应 Tx Height: %s", resp.Tx.GetHeight())
		log.Printf("收到响应 Tx ContractAddress: '%s'", resp.Tx.GetContractAddress())
		log.Printf("收到响应 Tx Datetime: %s", resp.Tx.GetDatetime())
		log.Printf("收到响应 Tx Data: %s", resp.Tx.GetData())
	} else {
		log.Printf("收到响应 Tx: nil")
	}

	// 或者更直接地打印整个 Tx 结构体
	// log.Printf("原始 Tx 结构体: %+v", resp.GetTx())

}
