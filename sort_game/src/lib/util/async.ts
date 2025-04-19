export const delay = async (miliseconds: number) => {
    return new Promise((resolve) => {
        window.setTimeout(() => {
            resolve(0);
        }, miliseconds);
    });
}