import dotenv from "dotenv";
// A devnet test wallet's recovery phrase, from MOI_MNEMONIC in the environment or a .env file next to this script.
// Never a wallet with real funds. Never commit the .env file.
dotenv.config({ quiet: true });
export const MNEMONIC = process.env.MOI_MNEMONIC;
if (!MNEMONIC) throw new Error("MOI_MNEMONIC not set (put a devnet test wallet's 12 words in .env)");
